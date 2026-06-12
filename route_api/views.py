"""
Route & Fuel Optimizer API View
================================
POST /api/route/optimize/
  Body: {"start": "New York, NY", "finish": "Los Angeles, CA"}
  Returns: route info, optimal fuel stops, total cost, map URL

GET /api/route/fuel-prices/
  Returns all state fuel prices
"""
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RouteRequestSerializer
from .services import (
    geocode_location,
    get_route,
    find_optimal_fuel_stops,
    build_map_url,
    load_fuel_prices,
    reverse_geocode,
    get_fuel_price_for_state,
)
from django.conf import settings


class RouteOptimizeView(APIView):
    """
    POST /api/route/optimize/

    Input:
        {
            "start": "Chicago, IL",
            "finish": "Houston, TX"
        }

    Output:
        Full route details, optimal fuel stops, total fuel cost, and map URL.
    """

    def post(self, request):
        t_start = time.time()

        serializer = RouteRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid input", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        start_loc = serializer.validated_data["start"]
        finish_loc = serializer.validated_data["finish"]

        try:
            # Step 1: Geocode both locations
            start_geo = geocode_location(start_loc)
            finish_geo = geocode_location(finish_loc)

            # Step 2: Get full route — ONE OSRM call
            route = get_route(
                start_geo["lat"], start_geo["lon"],
                finish_geo["lat"], finish_geo["lon"]
            )

            # Step 3: Get fuel price at start for initial fill-up
            start_state_info = reverse_geocode(start_geo["lat"], start_geo["lon"])
            start_state_code = start_state_info.get("state_code", "")
            start_fuel_price = get_fuel_price_for_state(start_state_code)

            # Step 4: Find optimal fuel stops along the route
            fuel_result = find_optimal_fuel_stops(route)

            # Step 5: Build map URL
            map_url = build_map_url(start_geo, finish_geo, fuel_result["fuel_stops"])

            elapsed = round(time.time() - t_start, 2)

            # Format duration nicely
            hrs = int(route["duration_hours"])
            mins = int((route["duration_hours"] - hrs) * 60)
            duration_str = f"{hrs}h {mins}m" if hrs else f"{mins}m"

            response_data = {
                "status": "success",
                "processing_time_seconds": elapsed,

                "trip": {
                    "start": {
                        "input": start_loc,
                        "display_name": start_geo["display_name"],
                        "lat": start_geo["lat"],
                        "lon": start_geo["lon"],
                        "state": start_state_info.get("state", ""),
                        "state_code": start_state_code,
                    },
                    "finish": {
                        "input": finish_loc,
                        "display_name": finish_geo["display_name"],
                        "lat": finish_geo["lat"],
                        "lon": finish_geo["lon"],
                    },
                    "distance_miles": route["distance_miles"],
                    "estimated_drive_time": duration_str,
                },

                "vehicle": {
                    "max_range_miles": settings.VEHICLE_MAX_RANGE_MILES,
                    "fuel_efficiency_mpg": settings.VEHICLE_MPG,
                    "total_gallons_needed": fuel_result["total_gallons"],
                },

                "fuel_stops": fuel_result["fuel_stops"],
                "fuel_stop_count": len(fuel_result["fuel_stops"]),

                "cost_summary": {
                    "total_fuel_cost_usd": fuel_result["total_fuel_cost_usd"],
                    "currency": "USD",
                    "note": f"Based on {settings.VEHICLE_MPG} MPG and state-level fuel prices",
                },

                "map": {
                    "url": map_url,
                    "description": "OpenStreetMap route with fuel stop waypoints",
                },
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Internal server error", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FuelPricesView(APIView):
    """
    GET /api/route/fuel-prices/
    Returns all US state fuel prices.
    """

    def get(self, request):
        prices = load_fuel_prices()
        data = [
            {
                "state_code": code,
                "state": info["state"],
                "price_per_gallon_usd": info["price_per_gallon"],
            }
            for code, info in sorted(prices.items(), key=lambda x: x[1]["price_per_gallon"])
        ]
        return Response({
            "status": "success",
            "count": len(data),
            "fuel_prices": data,
            "note": "Prices sorted cheapest to most expensive"
        })


class HealthCheckView(APIView):
    """GET /api/health/ — simple health check"""

    def get(self, request):
        return Response({"status": "ok", "service": "Fuel Route Optimizer API"})
