<<<<<<< HEAD
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
=======
<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:FF6B35,50:F7C59F,100:1A1A2E&height=220&section=header&text=⛽%20Fuel%20Route%20Optimizer%20API&fontSize=40&fontColor=ffffff&animation=twinkling&fontAlignY=38&desc=Smart%20fuel%20stop%20planning%20for%20any%20US%20road%20trip%20🗺️&descAlignY=60&descSize=16" width="100%"/>

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&duration=2500&pause=800&color=FF6B35&center=true&vCenter=true&multiline=true&width=650&height=90&lines=🐍+Django+REST+Framework+API;⛽+NY+→+LA+for+%24934.72+%7C+6+Optimized+Stops;🆓+Zero+API+Keys+%7C+100%25+Free+Routing" alt="Typing SVG" />
</a>

<br/>

<!-- Status Badges -->
<p>
  <img src="https://img.shields.io/badge/Django-4.x-092E20?style=for-the-badge&logo=django&logoColor=white&labelColor=0d1117"/>
  <img src="https://img.shields.io/badge/DRF-3.x-ff1709?style=for-the-badge&logo=django&logoColor=white&labelColor=0d1117"/>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0d1117"/>
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white&labelColor=0d1117"/>
</p>

<p>
  <img src="https://img.shields.io/badge/OSRM-Routing-7EBC6F?style=for-the-badge&logo=openstreetmap&logoColor=white&labelColor=0d1117"/>
  <img src="https://img.shields.io/badge/Nominatim-Geocoding-48A999?style=for-the-badge&logo=openstreetmap&logoColor=white&labelColor=0d1117"/>
  <img src="https://img.shields.io/badge/License-MIT-F7C59F?style=for-the-badge&labelColor=0d1117"/>
  <img src="https://img.shields.io/badge/Status-Active-00D26A?style=for-the-badge&labelColor=0d1117"/>
</p>

<!-- Live Demo Stats -->
<table>
<tr>
<td align="center"><img src="https://img.shields.io/badge/2%2C798-Total%20Miles-FF6B35?style=flat-square"/></td>
<td align="center"><img src="https://img.shields.io/badge/%24934.72-Fuel%20Cost-00D26A?style=flat-square"/></td>
<td align="center"><img src="https://img.shields.io/badge/6-Optimized%20Stops-3776AB?style=flat-square"/></td>
<td align="center"><img src="https://img.shields.io/badge/1-OSRM%20API%20Call-F7C59F?style=flat-square&labelColor=333"/></td>
</tr>
</table>

</div>

---

<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║  POST {"start": "New York, NY", "finish": "Los Angeles, CA"} ║
║  ──────────────────────────────────────────────────────────  ║
║  ✅  6 optimized stops  •  $934.72 total  •  2,798 miles     ║
╚══════════════════════════════════════════════════════════════╝
```

</div>

---

## 🌟 Features at a Glance

<div align="center">

|  🔍 Smart Routing  |  ⛽ Cost Optimizer  |  🆓 Free APIs  |  📡 Clean REST  |
|:------------------:|:-------------------:|:---------------:|:----------------:|
| Full polyline via 1 OSRM call | Samples 5 candidates per stop window | OSRM — no key needed | `POST /optimize/` |
| Haversine mile-marker precision | Picks cheapest state in ±100mi window | Nominatim — no key needed | `GET /fuel-prices/` |
| 500mi range + 50mi safety buffer | 10 MPG real cost calculation | SQLite — no DB server | `GET /health/` |

</div>

---

## ⚡ Quick Start

<details open>
<summary><b>🖥️ Run Locally</b></summary>

```bash
# Clone the repo
git clone https://github.com/engrmumtazali0112/Fuel-Route-Optimizer-API.git
cd Fuel-Route-Optimizer-API

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations & start server
python manage.py migrate
python manage.py runserver
```

> 🚀 API live at **`http://127.0.0.1:8000`**

</details>

<details>
<summary><b>🐳 Docker</b></summary>
>>>>>>> origin/main

```bash
docker build -t fuel-optimizer .
docker run -p 8000:8000 fuel-optimizer
```

<<<<<<< HEAD
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
=======
</details>

---

## 📡 API Reference

### `POST /api/route/optimize/` — Main Endpoint

```bash
curl -X POST http://127.0.0.1:8000/api/route/optimize/ \
  -H "Content-Type: application/json" \
  -d '{"start": "New York, NY", "finish": "Los Angeles, CA"}'
```

<details>
<summary><b>📥 Full Response Example</b></summary>

```json
{
  "status": "success",
  "processing_time_seconds": 48.62,
  "trip": {
    "start": { "display_name": "New York, United States", "lat": 40.71, "lon": -74.00, "state_code": "NY" },
    "finish": { "display_name": "Los Angeles, United States", "lat": 34.05, "lon": -118.24 },
    "distance_miles": 2798.4,
    "estimated_drive_time": "49h 47m"
  },
  "vehicle": { "max_range_miles": 500, "fuel_efficiency_mpg": 10, "total_gallons_needed": 279.82 },
  "fuel_stops": [
    { "stop_number": 1, "location": "Richfield, Ohio", "state_code": "OH",
      "mile_marker": 450, "price_per_gallon": 3.21, "gallons_needed": 45.0, "cost_usd": 144.45 }
  ],
  "cost_summary": { "total_fuel_cost_usd": 934.72, "currency": "USD" },
  "map": { "url": "https://www.openstreetmap.org/directions?..." }
}
```

</details>

### `GET /api/route/fuel-prices/` — All 50 State Prices

```json
{ "status": "success", "count": 50,
  "fuel_prices": [
    { "state_code": "TX", "state": "Texas", "price_per_gallon_usd": 3.02 },
    { "state_code": "MS", "state": "Mississippi", "price_per_gallon_usd": 3.03 }
>>>>>>> origin/main
  ]
}
```

<<<<<<< HEAD
---

### 3. `GET /api/health/`

Health check endpoint.
=======
### `GET /api/health/` — Health Check
>>>>>>> origin/main

```json
{ "status": "ok", "service": "Fuel Route Optimizer API" }
```

---

<<<<<<< HEAD
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
=======
## 🧠 How the Optimizer Works

```
 📍 START                                                    🏁 FINISH
  │                                                             │
  ▼                                                             ▼
┌─────────────┐    ┌─────────────┐    ┌──────────────────────────────────┐
│  Nominatim  │    │    OSRM     │    │       Fuel Optimizer Loop        │
│  Geocoding  │───▶│  1 API Call │───▶│  Every 450 miles:                │
│  (2 calls)  │    │  Full route │    │  • Sample 5 candidate points     │
└─────────────┘    │  + polyline │    │  • Reverse-geocode each → State  │
                   └─────────────┘    │  • Pick cheapest state price     │
                                      │  • Calculate gallons × price     │
                                      └──────────────────────────────────┘
                                                    │
                                                    ▼
                                      ┌──────────────────────────────────┐
                                      │  📊 Return: stops + cost + map   │
                                      └──────────────────────────────────┘
```

**Total external API calls:** ~3–8 for any cross-country trip ✅

---

## 📊 Live Demo — New York → Los Angeles

<div align="center">

| Field | Value |
|-------|-------|
| 📏 Total Distance | **2,798 miles** |
| ⏱️ Drive Time | **49 hrs 47 min** |
| ⛽ Total Gallons | **279.82 gal** |
| 💵 **Total Fuel Cost** | **$934.72 USD** |
| 🛑 Fuel Stops | **6 optimized** |

</div>

### 🗺️ Optimized Stop Breakdown

| # | 📍 Location | 🛣️ Mile | 💲/gal | 🪣 Gallons | 💰 Cost |
|:-:|------------|:-------:|:------:|:---------:|:------:|
| 1 | Richfield, **Ohio** | 450 | $3.21 | 45.0 | $144.45 |
| 2 | **Indiana** | 675 | $3.19 | 22.5 | $71.78 |
| 3 | Tiffin, **Iowa** | 1,013 | $3.14 | 33.75 | $105.98 |
| 4 | **Nebraska** | 1,350 | $3.13 | 33.75 | $105.64 |
| 5 | Denver, **Colorado** | 1,800 | $3.50 | 22.5 | $78.75 |
| 6 | Nevada/**AZ Border** | 2,475 | $3.50 | 22.5 | $78.75 |

---

## 🧪 Test Routes

```bash
# 🗽 New York → 🌴 Los Angeles  (~2,800 mi, 6 stops)
{"start": "New York, NY", "finish": "Los Angeles, CA"}

# 🌆 Chicago → 🌴 Miami  (~1,400 mi, 3 stops)
{"start": "Chicago, IL", "finish": "Miami, FL"}

# 🌲 Seattle → 🏔️ Denver  (~1,300 mi, 2 stops)
{"start": "Seattle, WA", "finish": "Denver, CO"}
```

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|-------|-----------|
| **Framework** | Django 4.x + Django REST Framework |
| **Geocoding** | Nominatim (OpenStreetMap) — free, no API key |
| **Routing** | OSRM (Open Source Routing Machine) — free, no API key |
| **Fuel Data** | CSV file — all 50 US states |
| **Distance Calc** | Haversine formula |
| **Database** | SQLite |
| **Containerization** | Docker |
| **Map Output** | OpenStreetMap directions URL |

</div>
>>>>>>> origin/main

---

## 🗂️ Project Structure

```
<<<<<<< HEAD
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
=======
Fuel-Route-Optimizer-API/
├── 📄 manage.py
├── 📦 requirements.txt
├── 🐳 Dockerfile
├── 📋 README.md
├── data/
│   └── 📊 fuel_prices.csv        ← All 50 US state gas prices
├── fuel_optimizer/
│   ├── ⚙️  settings.py
│   ├── 🔗 urls.py
│   └── 🚀 wsgi.py
└── route_api/
    ├── 👁️  views.py               ← API endpoint handlers
    ├── 🧠 services.py             ← Core optimizer logic
    ├── ✅ serializers.py          ← Input validation
    └── 🔗 urls.py
>>>>>>> origin/main
```

---

<<<<<<< HEAD
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
=======
## 👤 Author

<div align="center">

<img src="https://avatars.githubusercontent.com/u/engrmumtazali0112" width="80" style="border-radius:50%"/>

### Mumtaz Ali
**Full Stack AI/ML Developer · Lahore, Pakistan**

[![GitHub](https://img.shields.io/badge/GitHub-engrmumtazali0112-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/engrmumtazali0112)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Mumtaz%20Ali-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/mumtazali12)
[![Email](https://img.shields.io/badge/Email-engrmumtazali01%40gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:engrmumtazali01@gmail.com)

*Django · FastAPI · React · Flutter · PostgreSQL · AWS*

</div>

---

<div align="center">

**⭐ Star this repo if it saved you money on your next road trip!**

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1A1A2E,50:FF6B35,100:F7C59F&height=100&section=footer&animation=twinkling" width="100%"/>

</div>
>>>>>>> origin/main
