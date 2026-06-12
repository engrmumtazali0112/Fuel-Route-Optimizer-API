# 🛣️ Fuel Route Optimizer API

A Django REST API that calculates the optimal fuel stops for a road trip across the USA, minimizing fuel costs based on state-level gas prices.

---

## 🚀 Quick Start

### Option 1: Run Locally

```bash
# 1. Clone / unzip the project
cd fuel_optimizer

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations (minimal — no DB models used)
python manage.py migrate

# 5. Start the server
python manage.py runserver
```

API is now live at: `http://127.0.0.1:8000`

### Option 2: Docker

```bash
docker build -t fuel-optimizer .
docker run -p 8000:8000 fuel-optimizer
```

---

## 📡 API Endpoints

### 1. `POST /api/route/optimize/`

**The main endpoint.** Takes start and finish locations, returns optimal fuel stops and total cost.

**Request Body:**
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
  "processing_time_seconds": 3.21,
  "trip": {
    "start": {
      "input": "New York, NY",
      "display_name": "New York, New York, United States",
      "lat": 40.7127281,
      "lon": -74.0060152,
      "state": "New York",
      "state_code": "NY"
    },
    "finish": {
      "input": "Los Angeles, CA",
      "display_name": "Los Angeles, California, United States",
      "lat": 34.0536909,
      "lon": -118.2427666
    },
    "distance_miles": 2790.5,
    "estimated_drive_time": "40h 12m"
  },
  "vehicle": {
    "max_range_miles": 500,
    "fuel_efficiency_mpg": 10,
    "total_gallons_needed": 279.05
  },
  "fuel_stops": [
    {
      "stop_number": 1,
      "location": {
        "lat": 40.44,
        "lon": -80.01,
        "city": "Pittsburgh",
        "state": "Pennsylvania",
        "state_code": "PA"
      },
      "mile_marker": 337.5,
      "price_per_gallon": 3.49,
      "gallons_needed": 33.75,
      "cost_usd": 117.82
    }
  ],
  "fuel_stop_count": 6,
  "cost_summary": {
    "total_fuel_cost_usd": 952.40,
    "currency": "USD",
    "note": "Based on 10 MPG and state-level fuel prices"
  },
  "map": {
    "url": "https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route=...",
    "description": "OpenStreetMap route with fuel stop waypoints"
  }
}
```

---

### 2. `GET /api/route/fuel-prices/`

Returns all US state fuel prices, sorted cheapest to most expensive.

**Response:**
```json
{
  "status": "success",
  "count": 50,
  "fuel_prices": [
    { "state_code": "MS", "state": "Mississippi", "price_per_gallon_usd": 3.03 },
    { "state_code": "TX", "state": "Texas", "price_per_gallon_usd": 3.02 }
  ]
}
```

---

### 3. `GET /api/health/`

Health check endpoint.

```json
{ "status": "ok", "service": "Fuel Route Optimizer API" }
```

---

## 🧠 How It Works

### Architecture

```
Client → Django REST API
              ↓
       1. Nominatim (OSM) — geocode start/finish (free, no key)
       2. OSRM — ONE routing call to get full route + polyline
       3. Fuel Optimizer Algorithm — finds optimal stop points
       4. Nominatim reverse geocode — identify state at each stop
       5. Fuel Price Lookup — CSV file with state prices
       6. Return result with map URL
```

### Optimization Algorithm

1. **Divide** the route into segments of up to **450 miles** (500 mile max range, 50-mile safety buffer)
2. **Sample 5 candidate points** evenly across each refuel window
3. **Reverse-geocode** each candidate to identify the US state
4. **Select the cheapest state** within the window as the fuel stop
5. **Calculate cost** = (miles / 10 MPG) × price per gallon

### API Calls Strategy (Minimizing External Calls)
- **1 call** to OSRM (full route with polyline)
- **2 calls** to Nominatim for geocoding (start + finish)
- **~5 calls** per fuel stop for reverse geocoding candidates
- Total: **~3–8 external calls** for a typical cross-country trip ✅

### Free APIs Used (No API Keys Required)
| Service | Purpose | URL |
|---------|---------|-----|
| Nominatim | Geocoding | nominatim.openstreetmap.org |
| OSRM | Routing & Polyline | router.project-osrm.org |

---

## 📊 Vehicle Assumptions

| Parameter | Value |
|-----------|-------|
| Max Range | 500 miles |
| Fuel Efficiency | 10 MPG |
| Refuel Trigger | Every 450 miles (50-mile buffer) |

---

## 🗂️ Project Structure

```
fuel_optimizer/
├── manage.py
├── requirements.txt
├── Dockerfile
├── README.md
├── data/
│   └── fuel_prices.csv          # US state fuel prices
├── fuel_optimizer/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── route_api/
    ├── views.py                  # API endpoints
    ├── services.py               # Core logic: routing, geocoding, optimization
    ├── serializers.py            # Input validation
    └── urls.py
```

---

## 🧪 Testing with Postman

### Example Requests

**New York → Los Angeles (2,800 miles, ~6 stops):**
```
POST http://127.0.0.1:8000/api/route/optimize/
Content-Type: application/json

{"start": "New York, NY", "finish": "Los Angeles, CA"}
```

**Chicago → Miami (1,400 miles, ~3 stops):**
```
POST http://127.0.0.1:8000/api/route/optimize/
Content-Type: application/json

{"start": "Chicago, IL", "finish": "Miami, FL"}
```

**Seattle → Denver (1,300 miles, ~2 stops):**
```
POST http://127.0.0.1:8000/api/route/optimize/
Content-Type: application/json

{"start": "Seattle, WA", "finish": "Denver, CO"}
```

---

## 📝 Author

**Mumtaz Ali** — Full Stack AI/ML Developer  
engrmumtazali01@gmail.com | github.com/engrmumtazali0112
