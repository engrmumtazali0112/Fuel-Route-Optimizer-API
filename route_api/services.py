"""
Services for geocoding, routing, and fuel optimization.
Uses:
  - Nominatim (OpenStreetMap) for geocoding - free, no key
  - OSRM for routing - free, no key
  - Custom fuel price algorithm for optimization
"""
import csv
import math
import requests
from django.conf import settings


# ─────────────────────────────────────────────
# 1. GEOCODING  (Nominatim - free, no API key)
# ─────────────────────────────────────────────
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_REVERSE_URL = "https://nominatim.openstreetmap.org/reverse"
HEADERS = {"User-Agent": "FuelOptimizerDjango/1.0 (engrmumtazali01@gmail.com)"}


def geocode_location(location: str) -> dict:
    """Return {lat, lon, display_name} for a US location string."""
    params = {
        "q": location,
        "format": "json",
        "countrycodes": "us",
        "limit": 1,
    }
    resp = requests.get(NOMINATIM_URL, params=params, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    results = resp.json()
    if not results:
        raise ValueError(f"Could not geocode location: '{location}'")
    r = results[0]
    return {"lat": float(r["lat"]), "lon": float(r["lon"]), "display_name": r["display_name"]}


def reverse_geocode(lat: float, lon: float) -> dict:
    """Return address info for coordinates."""
    params = {"lat": lat, "lon": lon, "format": "json"}
    resp = requests.get(NOMINATIM_REVERSE_URL, params=params, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    address = data.get("address", {})
    return {
        "display_name": data.get("display_name", ""),
        "state": address.get("state", ""),
        "state_code": address.get("ISO3166-2-lvl4", "").replace("US-", ""),
        "city": address.get("city") or address.get("town") or address.get("village") or "",
    }


# ─────────────────────────────────────────────
# 2. ROUTING  (OSRM - free, no API key)
#    ONE call to get full route geometry + distance
# ─────────────────────────────────────────────
OSRM_BASE = "http://router.project-osrm.org"


def get_route(start_lat, start_lon, end_lat, end_lon) -> dict:
    """
    Single OSRM call: returns route distance (miles), duration (seconds),
    and polyline coordinates list [(lat,lon), ...].
    """
    coords = f"{start_lon},{start_lat};{end_lon},{end_lat}"
    url = f"{OSRM_BASE}/route/v1/driving/{coords}"
    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "false",
    }
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    if data.get("code") != "Ok":
        raise ValueError(f"OSRM routing error: {data.get('message', 'Unknown error')}")

    route = data["routes"][0]
    distance_meters = route["distance"]
    distance_miles = distance_meters * 0.000621371
    duration_seconds = route["duration"]

    # GeoJSON coordinates are [lon, lat] - flip to (lat, lon)
    coords_list = [
        (pt[1], pt[0])
        for pt in route["geometry"]["coordinates"]
    ]

    return {
        "distance_miles": round(distance_miles, 2),
        "duration_seconds": int(duration_seconds),
        "duration_hours": round(duration_seconds / 3600, 2),
        "polyline": coords_list,  # list of (lat, lon)
    }


# ─────────────────────────────────────────────
# 3. FUEL PRICES  (from CSV)
# ─────────────────────────────────────────────
_FUEL_PRICES_CACHE = None


def load_fuel_prices() -> dict:
    """Load state fuel prices from CSV. Cached after first load."""
    global _FUEL_PRICES_CACHE
    if _FUEL_PRICES_CACHE is not None:
        return _FUEL_PRICES_CACHE

    prices = {}
    with open(settings.FUEL_DATA_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prices[row["state_code"].strip().upper()] = {
                "state": row["state"].strip(),
                "price_per_gallon": float(row["price_per_gallon"]),
            }
    _FUEL_PRICES_CACHE = prices
    return prices


def get_fuel_price_for_state(state_code: str) -> float:
    """Return price per gallon for a US state code. Default 3.50 if unknown."""
    prices = load_fuel_prices()
    info = prices.get(state_code.upper())
    return info["price_per_gallon"] if info else 3.50


# ─────────────────────────────────────────────
# 4. HAVERSINE DISTANCE
# ─────────────────────────────────────────────
def haversine_miles(lat1, lon1, lat2, lon2) -> float:
    """Distance in miles between two lat/lon points."""
    R = 3958.8  # Earth radius miles
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


# ─────────────────────────────────────────────
# 5. FUEL STOP OPTIMIZER
# ─────────────────────────────────────────────
MAX_RANGE = settings.VEHICLE_MAX_RANGE_MILES   # 500 miles
MPG = settings.VEHICLE_MPG                      # 10 mpg
# We refuel at 450 miles to keep a safe 50-mile buffer
REFUEL_INTERVAL = 450


def _interpolate_point(polyline: list, target_miles: float, total_miles: float):
    """
    Walk the polyline and find the (lat, lon) at `target_miles` along the route.
    Returns (lat, lon, actual_miles_along_route).
    """
    if not polyline or total_miles == 0:
        return polyline[0][0], polyline[0][1], 0.0

    accumulated = 0.0
    for i in range(len(polyline) - 1):
        lat1, lon1 = polyline[i]
        lat2, lon2 = polyline[i + 1]
        seg_dist = haversine_miles(lat1, lon1, lat2, lon2)

        if accumulated + seg_dist >= target_miles:
            # Interpolate within this segment
            fraction = (target_miles - accumulated) / seg_dist if seg_dist > 0 else 0
            lat = lat1 + fraction * (lat2 - lat1)
            lon = lon1 + fraction * (lon2 - lon1)
            return lat, lon, target_miles

        accumulated += seg_dist

    # Past the end - return last point
    return polyline[-1][0], polyline[-1][1], accumulated


def find_optimal_fuel_stops(route: dict) -> dict:
    """
    Given the route dict from get_route(), determine optimal fuel stops
    every REFUEL_INTERVAL miles (or less at end), choosing cheapest state.

    Strategy:
      - Divide route into segments of up to REFUEL_INTERVAL miles
      - For each segment, sample several points along it
      - Reverse-geocode sampled points to find states
      - Pick the point in the cheapest-priced state within range
      - Only one Nominatim call per fuel stop (cheapest point)
    """
    total_miles = route["distance_miles"]
    polyline = route["polyline"]

    fuel_stops = []
    # ── FIX: use a deterministic mile counter, not best["mile"] ──
    # Plan stop positions upfront: 450, 900, 1350, ... up to total_miles
    stop_positions = []
    pos = REFUEL_INTERVAL
    while pos < total_miles:
        stop_positions.append(pos)
        pos += REFUEL_INTERVAL

    stop_number = 0
    prev_mile = 0.0

    for target_mile in stop_positions:
        # Search window: look REFUEL_INTERVAL/2 back and forward for cheapest state
        window_start = max(prev_mile + 50, target_mile - 100)
        window_end = min(target_mile + 100, total_miles - 10)

        if window_start >= window_end:
            window_start = target_mile - 50
            window_end = target_mile + 50

        # Sample 5 candidate points evenly across the window
        candidates = []
        num_samples = 5
        for i in range(num_samples):
            frac = i / (num_samples - 1) if num_samples > 1 else 0.5
            sample_mile = window_start + (window_end - window_start) * frac
            lat, lon, actual = _interpolate_point(polyline, sample_mile, total_miles)
            candidates.append({"lat": lat, "lon": lon, "mile": actual})

        # Reverse-geocode each candidate to find state
        best = None
        best_price = float("inf")
        for c in candidates:
            try:
                geo = reverse_geocode(c["lat"], c["lon"])
                state_code = geo.get("state_code", "")
                price = get_fuel_price_for_state(state_code) if state_code else 3.50
                c["state_code"] = state_code
                c["state"] = geo.get("state", "")
                c["city"] = geo.get("city", "")
                c["price_per_gallon"] = price
                if price < best_price:
                    best_price = price
                    best = c
            except Exception:
                continue

        if best is None:
            # Fallback: stop at the target mile
            lat, lon, actual = _interpolate_point(polyline, target_mile, total_miles)
            best = {
                "lat": lat, "lon": lon, "mile": actual,
                "state_code": "XX", "state": "Unknown",
                "city": "", "price_per_gallon": 3.50,
            }

        stop_number += 1
        gallons_since_last = (best["mile"] - prev_mile) / MPG
        cost = gallons_since_last * best["price_per_gallon"]

        fuel_stops.append({
            "stop_number": stop_number,
            "location": {
                "lat": round(best["lat"], 5),
                "lon": round(best["lon"], 5),
                "city": best.get("city", ""),
                "state": best.get("state", ""),
                "state_code": best.get("state_code", ""),
            },
            "mile_marker": round(best["mile"], 1),
            "price_per_gallon": best["price_per_gallon"],
            "gallons_needed": round(gallons_since_last, 2),
            "cost_usd": round(cost, 2),
        })

        prev_mile = best["mile"]

    # Final leg cost - from last stop to destination
    remaining_miles = total_miles - prev_mile
    if remaining_miles > 0 and fuel_stops:
        last_stop_price = fuel_stops[-1]["price_per_gallon"]
    else:
        last_stop_price = 3.50

    total_gallons = total_miles / MPG
    total_cost = sum(s["cost_usd"] for s in fuel_stops)

    if remaining_miles > 0:
        final_cost = (remaining_miles / MPG) * last_stop_price
        total_cost += final_cost

    return {
        "fuel_stops": fuel_stops,
        "total_gallons": round(total_gallons, 2),
        "total_fuel_cost_usd": round(total_cost, 2),
    }


# ─────────────────────────────────────────────
# 6. MAP URL GENERATOR
# ─────────────────────────────────────────────
def build_map_url(start: dict, end: dict, fuel_stops: list) -> str:
    """
    Build an OpenStreetMap-based map URL showing the route.
    Returns a shareable link to a pre-drawn route on OpenStreetMap.
    """
    start_str = f"{start['lat']},{start['lon']}"
    end_str = f"{end['lat']},{end['lon']}"

    waypoints = ""
    for stop in fuel_stops:
        loc = stop["location"]
        waypoints += f"%3B{loc['lat']}%2C{loc['lon']}"

    map_url = (
        f"https://www.openstreetmap.org/directions?"
        f"engine=fossgis_osrm_car&route={start_str}{waypoints}%3B{end_str}"
    )
    return map_url