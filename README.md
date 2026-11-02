# 🛡️ TravelGuardian AI — Smart Tourism & Tourist Safety Platform

> **An advanced, real-time web application providing AI-powered travel recommendations, crowd density forecasting, safety intelligence scanner, live Open-Meteo weather updates, emergency GPS SOS tracking, digital wallet, ticket booking, and an interactive AI Voice Call hotline.**

---

## 🌟 Key Highlights & Architecture

- **🎨 Modern Glassmorphic Dashboard (SPA):** Built with Flask backend and a responsive Single Page Application (SPA) frontend featuring dark mode glassmorphic UI, micro-animations, and custom styling.
- **🔐 Dedicated Authentication Portal:** Complete user registration and login system backed by SQLite database with bcrypt password hashing. New user registrations automatically receive a **₹10,000 Demo Wallet Bonus**.
- **🌤️ Real-Time Open-Meteo Weather Integration:** Live temperature (°C), humidity, wind speed, and WMO climate condition codes fetched directly via the Open-Meteo API.
- **🎙️ AI Voice Call Hotline:** Interactive voice support powered by Web Speech Synthesis (`SpeechSynthesisUtterance`) and Speech Recognition (`webkitSpeechRecognition`) for hands-free live audio responses and emergency sirens.
- **📍 Real-Time GPS Emergency SOS:** Browser Geolocation API integration providing precise GPS coordinates (`Lat/Lon`), Leaflet map tracking, and 1-click distress alert broadcasts via WhatsApp.
- **📊 Real-Time Interactive Analytics:** Visual charts powered by Chart.js for hourly crowd curves, multi-factor safety risk breakdowns, and trip expense distribution.

---

## ⚡ Core Features

1. **🧭 AI Trip Planner & Itinerary Generator**
   - Match Indian travel destinations based on total budget, duration, preferred season, and interests.
   - Generates day-by-day customized itineraries and shows live weather updates.

2. **📊 Real-Time Crowd Density Radar**
   - Predicts congestion levels (Critical, Elevated, Moderate, Quiet) for major Indian tourist hubs.
   - Renders an 8:00 AM – 10:00 PM hourly projection curve chart.

3. **🛡️ Tourist Safety Scanner**
   - Multi-dimensional safety matrix calculating crime rate, healthcare access, transport security, and solo female traveler scores.
   - Adjusts risk dynamically based on daytime vs. nighttime travel windows.

4. **💰 Trip Cost Estimator & Budget Planner**
   - Accurate expense forecasting across Stay/Hotel, Dining, Local Transit, Activities, and Emergency Buffers.
   - Displays donut pie chart distribution and per-person cost calculations.

5. **📞 AI Voice Call Hotline**
   - Live simulated incoming call modal with glowing microphone wave animations.
   - Real-time speech recognition input and natural voice audio responses.
   - Quick triggers for Safety Audio Briefings and Emergency Siren Alarms.

6. **🎫 Smart Ticket Booking & Digital Boarding Passes**
   - Book Flights, Trains, Buses, or Hotels using your digital wallet balance.
   - Automatic refund calculation for booking cancellations.

7. **💳 Digital Demo Wallet & Audit Ledger**
   - Seamless wallet top-ups, live balance display, and structured transaction history.

8. **👑 Admin Command Center**
   - System metrics monitoring total registered users, active bookings, cancellations, and overall wallet float.

---

## 🚀 Quick Setup & Installation Guide

### 1. Clone or Extract Project
Navigate to the project root directory:
```bash
cd TravelGuardianAI
```

### 2. Create and Activate Virtual Environment
**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Web Server
```bash
python server.py
```

### 5. Access the Web Dashboard
Open your web browser and navigate to:
```
http://localhost:8000
```

---

## 🔑 Demo Account Credentials

| Role | Email | Password | Perks |
| :--- | :--- | :--- | :--- |
| **Standard User** | `user@tg.ai` | `user123` | Pre-funded ₹20,000 Wallet |
| **Admin Officer** | `admin@tg.ai` | `admin123` | Full Access to Admin Control Panel |

> *Note: You can also click **Create Account** on the login page to register a brand-new real account instantly with a ₹10,000 bonus.*

---

## 📁 Project Directory Structure

```
TravelGuardianAI/
│
├── server.py              # Flask Web Server & REST API endpoints
├── ai_engine.py            # AI Engine, Open-Meteo Weather API, Safety & Crowd Logic
├── db.py                  # SQLite Database persistence layer & user auth
├── requirements.txt       # Python dependencies (Flask, requests, bcrypt, etc.)
├── travelguardian.db      # SQLite database file (Auto-generated on start)
│
└── templates/
    └── index.html         # Glassmorphic HTML5 SPA Dashboard (Leaflet, Chart.js, Speech API)
```

---

## 🔌 REST API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/login` | Authenticate user credentials against SQLite DB |
| `POST` | `/api/signup` | Register new user account & seed initial wallet bonus |
| `POST` | `/api/recommend` | Generate AI destination recommendations & itineraries |
| `POST` | `/api/crowd` | Compute destination crowd density & hourly curve |
| `POST` | `/api/safety` | Calculate safety index score & risk factors |
| `POST` | `/api/budget` | Estimate trip budget breakdown |
| `POST` | `/api/assistant` | Query AI travel assistant response |
| `GET` | `/api/destinations` | Fetch list of Indian destinations with real-time weather |
| `GET` | `/api/wallet/<uid>` | Fetch wallet balance & transaction ledger |
| `POST` | `/api/wallet/topup` | Top-up digital wallet balance |
| `GET` | `/api/bookings/<uid>` | Fetch user bookings |
| `POST` | `/api/bookings/create` | Create a new ticket booking |
| `POST` | `/api/bookings/cancel` | Cancel booking & issue refund |
| `GET` | `/api/admin/stats` | Retrieve system-wide analytics for admin panel |

---

## 🛡️ Emergency Helplines (India)

- **Universal Emergency:** `112`
- **Police Helpline:** `100`
- **Medical Ambulance:** `108`
- **Women Safety Helpline:** `1091`
- **National Tourist Helpline:** `1363`

---

## 📄 License
This project is licensed under the MIT License - feel free to customize and expand for smart tourism and safety initiatives.
