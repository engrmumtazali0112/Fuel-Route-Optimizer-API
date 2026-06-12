<div align="center">

<!-- Animated Header Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=⛽%20Fuel%20Route%20Optimizer%20API&fontSize=42&fontColor=fff&animation=twinkling&fontAlignY=36&desc=Minimize%20fuel%20costs%20on%20any%20US%20road%20trip%20with%20smart%20stop%20optimization&descAlignY=58&descSize=16" width="100%"/>

<!-- Animated Typing -->
<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3000&pause=1000&color=F7A51A&center=true&vCenter=true&multiline=true&width=600&height=80&lines=Django+REST+API+%F0%9F%90%8D;Smart+Fuel+Stop+Optimizer+%E2%9B%BD;NY+%E2%86%92+LA+for+%24934.72+%F0%9F%9B%A3%EF%B8%8F" alt="Typing SVG" /></a>

<!-- Badges Row 1 -->
<p>
  <img src="https://img.shields.io/badge/Django-4.x-092E20?style=for-the-badge&logo=django&logoColor=white"/>
  <img src="https://img.shields.io/badge/DRF-3.x-ff1709?style=for-the-badge&logo=django&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
</p>

<!-- Badges Row 2 -->
<p>
  <img src="https://img.shields.io/badge/OSRM-Routing-blue?style=for-the-badge&logo=openstreetmap&logoColor=white"/>
  <img src="https://img.shields.io/badge/Nominatim-Geocoding-7EBC6F?style=for-the-badge&logo=openstreetmap&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge"/>
</p>

<!-- Live Demo Stats -->
<p>
  <img src="https://img.shields.io/badge/NY%20→%20LA-2%2C798%20miles-orange?style=flat-square&logo=google-maps"/>
  <img src="https://img.shields.io/badge/Fuel%20Cost-%24934.72-green?style=flat-square&logo=dollar-sign"/>
  <img src="https://img.shields.io/badge/Stops-6%20Optimized-blue?style=flat-square&logo=map-pin"/>
  <img src="https://img.shields.io/badge/API%20Calls-Minimal-purple?style=flat-square"/>
</p>

</div>

---

## 🗺️ What This Does

> **Given any two US cities, find the cheapest way to fuel your road trip.**

The Fuel Route Optimizer calculates your full driving route, figures out where you'll need to stop for gas based on your vehicle's range, then picks stops in states with the **lowest gas prices** — saving you real money on every long-distance trip.

```
POST /api/route/optimize/
{ "start": "New York, NY", "finish": "Los Angeles, CA" }

→ 6 optimized stops  →  $934.72 total  →  OpenStreetMap route link
```

---

## ✨ Features

<table>
<tr>
<td width="50%">

**🔍 Smart Route Planning**
- Full driving route via OSRM (1 API call)
- Geocoding via Nominatim/OpenStreetMap
- Haversine formula for precise mile markers
- 500-mile range with 50-mile safety buffer

</td>
<td width="50%">

**⛽ Fuel Cost Optimization**
- State-level fuel prices from CSV (all 50 states)
- Samples 5 candidates per stop window
- Picks cheapest-state stop in ±100 mile window
- 10 MPG calculation for real cost estimates

</td>
</tr>
<tr>
<td width="50%">

**🆓 100% Free APIs**
- OSRM — no API key needed
- Nominatim — no API key needed
- No paid services required
- Runs fully on SQLite locally

</td>
<td width="50%">

**📡 Clean REST Endpoints**
- `GET /api/health/` — service check
- `GET /api/route/fuel-prices/` — all 50 state prices
- `POST /api/route/optimize/` — main optimizer

</td>
</tr>
</table>

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/engrmumtazali0112/Fuel-Route-Optimizer-API.git
cd Fuel-Route-Optimizer-API
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run

```bash
python manage.py migrate
python manage.py runserver
```

### 3. Test It

```bash
curl -X POST http://127.0.0.1:8000/api/route/optimize/ \
  -H "Content-Type: application/json" \
  -d '{"start": "New York, NY", "finish": "Los Angeles, CA"}'
```

---

## 📡 API Reference

### `POST /api/route/optimize/`

**Request:**
```json
{
  "start": "New York, NY",
  "finish": "Los Angeles, CA"
}
```

**Response:**
```json
{
  "status": "success",
  "processing_time_seconds": 48.62,
  "trip": {
    "start": { "display_name": "New York, United States", "lat": 40.71, "lon": -74.00 },
    "finish": { "display_name": "Los Angeles, United States", "lat": 34.05, "lon": -118.24 },
    "total_distance_miles": 2798.4,
    "estimated_drive_time": "49 hours 47 minutes"
  },
  "vehicle": {
    "max_range_miles": 500,
    "mpg": 10,
    "total_gallons_needed": 279.82
  },
  "fuel_stops": [
    {
      "stop_number": 1,
      "location": "Richfield, Ohio",
      "state": "OH",
      "mile_marker": 450,
      "price_per_gallon": 3.21,
      "gallons_needed": 45.0,
      "cost_usd": 144.45
    }
  ],
  "cost_summary": {
    "total_fuel_cost_usd": 934.72
  },
  "map": {
    "url": "https://www.openstreetmap.org/directions?..."
  }
}
```

### `GET /api/route/fuel-prices/`

Returns all 50 US state fuel prices, sorted cheapest first:

```json
{
  "status": "success",
  "count": 50,
  "fuel_prices": [
    { "state_code": "TX", "state": "Texas", "price_per_gallon_usd": 3.02 },
    { "state_code": "MS", "state": "Mississippi", "price_per_gallon_usd": 3.03 }
  ]
}
```

### `GET /api/health/`

```json
{ "status": "ok", "service": "Fuel Route Optimizer API" }
```

---

## 🗂️ Project Structure

```
Fuel-Route-Optimizer-API/
├── fuel_optimizer/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── routes/
│   ├── views.py          # API endpoint handlers
│   ├── services.py       # Core optimization logic
│   ├── serializers.py    # DRF serializers
│   └── urls.py
├── data/
│   └── fuel_prices.csv   # State-level gas prices (all 50 states)
├── manage.py
└── requirements.txt
```

---

## 🧠 How the Optimization Works

```
1. GEOCODE  →  Convert city names to lat/lon (Nominatim)
2. ROUTE    →  Get full polyline from OSRM (1 API call)
3. PLAN     →  Pre-calculate stop positions every 450 miles
4. SAMPLE   →  For each stop: sample 5 candidates in ±100mi window
5. PICK     →  Reverse-geocode each → identify state → pick cheapest
6. CALC     →  Gallons = miles / 10 MPG → Cost = gallons × price
7. RETURN   →  Full itinerary + total cost + OpenStreetMap URL
```

**Why 450 miles instead of 500?** A 50-mile safety buffer ensures you never hit empty in the middle of nowhere.

---

## 📊 Live Demo — New York → Los Angeles

| Field | Value |
|-------|-------|
| 📏 Total Distance | 2,798 miles |
| ⏱️ Drive Time | 49 hrs 47 min |
| ⛽ Total Gallons | 279.82 gal |
| 💵 **Total Fuel Cost** | **$934.72 USD** |
| 🛑 Fuel Stops | 6 optimized stops |
| ✅ API Status | 200 OK |

### Optimized Stop Breakdown

| # | Location | Mile | $/gal | Gallons | Cost |
|---|----------|------|-------|---------|------|
| 1 | Richfield, Ohio | 450 | $3.21 | 45.0 | $144.45 |
| 2 | Indiana | 675 | $3.19 | 22.5 | $71.78 |
| 3 | Tiffin, Iowa | 1,013 | $3.14 | 33.75 | $105.98 |
| 4 | Nebraska | 1,350 | $3.13 | 33.75 | $105.64 |
| 5 | Denver, Colorado | 1,800 | $3.50 | 22.5 | $78.75 |
| 6 | Nevada/AZ Border | 2,475 | $3.50 | 22.5 | $78.75 |

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|-------|-----------|
| **Framework** | Django 4.x + Django REST Framework |
| **Geocoding** | Nominatim (OpenStreetMap) — free, no key |
| **Routing** | OSRM (Open Source Routing Machine) — free, no key |
| **Fuel Data** | CSV (50 US states) |
| **Interpolation** | Haversine formula |
| **Database** | SQLite |
| **Map Output** | OpenStreetMap directions URL |

</div>

---

## 📋 Requirements Checklist

- [x] Built with latest stable Django (4.x)
- [x] `POST /api/route/optimize/` — start & finish location inputs
- [x] Returns optimal fuel stop locations
- [x] 500-mile max vehicle range handled (450-mile refuel interval)
- [x] Returns total fuel cost in USD (10 MPG)
- [x] Uses provided fuel prices CSV
- [x] Map/route API called minimally (1 OSRM call per request)
- [x] Free routing API found independently (OSRM + Nominatim)
- [x] `GET /api/route/fuel-prices/` — fuel prices endpoint

---

## 👤 Author

<div align="center">

**Mumtaz Ali**

[![GitHub](https://img.shields.io/badge/GitHub-engrmumtazali0112-181717?style=for-the-badge&logo=github)](https://github.com/engrmumtazali0112)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Mumtaz%20Ali-0077B5?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/mumtazali)
[![Email](https://img.shields.io/badge/Email-engrmumtazali01%40gmail.com-D14836?style=for-the-badge&logo=gmail)](mailto:engrmumtazali01@gmail.com)

*Full Stack Developer — Python | Django | React | Flutter*

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer&animation=twinkling" width="100%"/>

**⭐ Star this repo if it saved you money on your next road trip!**

</div>
