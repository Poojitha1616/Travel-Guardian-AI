"""AI engine: Gemini + real-time weather + safety + crowd + budget + itinerary + geospatial intelligence."""
import os
import requests
from datetime import datetime, timedelta

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
if GEMINI_AVAILABLE and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception:
        pass

INDIAN_DESTINATIONS = [
    {
        "name": "Goa",
        "state": "Goa",
        "lat": 15.2993,
        "lon": 74.1240,
        "interests": ["beach", "nightlife", "food", "water sports", "party", "culture"],
        "best_season": ["winter", "monsoon", "summer", "spring"],
        "avg_cost": 2200,
        "safety": 85,
        "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&auto=format&fit=crop&q=80",
        "description": "Sun-kissed beaches, Portuguese heritage churches, vibrant beach shacks and tropical nightlife."
    },
    {
        "name": "Manali",
        "state": "Himachal Pradesh",
        "lat": 32.2432,
        "lon": 77.1892,
        "interests": ["mountains", "adventure", "snow", "trekking", "nature"],
        "best_season": ["summer", "winter", "spring"],
        "avg_cost": 2500,
        "safety": 90,
        "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600&auto=format&fit=crop&q=80",
        "description": "Nestled in the Beas River valley, famed for Solang skiing, Rohtang snow peaks and pine forests."
    },
    {
        "name": "Jaipur",
        "state": "Rajasthan",
        "lat": 26.9124,
        "lon": 75.7873,
        "interests": ["heritage", "culture", "food", "royal", "shopping"],
        "best_season": ["winter", "spring"],
        "avg_cost": 1800,
        "safety": 82,
        "image": "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?w=600&auto=format&fit=crop&q=80",
        "description": "The Pink City featuring magnificent Amber Fort, Hawa Mahal, royal palaces, and rich artisanal bazaars."
    },
    {
        "name": "Kerala Backwaters",
        "state": "Kerala",
        "lat": 9.4981,
        "lon": 76.3388,
        "interests": ["nature", "beach", "food", "relaxation", "ayurveda"],
        "best_season": ["winter", "monsoon"],
        "avg_cost": 3000,
        "safety": 89,
        "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=600&auto=format&fit=crop&q=80",
        "description": "Tranquil network of canals, Alleppey houseboats, palm-lined shores, and soothing Ayurvedic wellness."
    },
    {
        "name": "Varanasi",
        "state": "Uttar Pradesh",
        "lat": 25.3176,
        "lon": 82.9739,
        "interests": ["spiritual", "heritage", "culture", "photography", "temples"],
        "best_season": ["winter", "spring"],
        "avg_cost": 1200,
        "safety": 78,
        "image": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=600&auto=format&fit=crop&q=80",
        "description": "One of the world's oldest living cities, spiritual Ganga Ghats, mesmerizing evening Aarti, and ancient alleys."
    },
    {
        "name": "Udaipur",
        "state": "Rajasthan",
        "lat": 24.5854,
        "lon": 73.7125,
        "interests": ["heritage", "romantic", "culture", "lakes", "royal"],
        "best_season": ["winter", "spring"],
        "avg_cost": 2400,
        "safety": 88,
        "image": "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?w=600&auto=format&fit=crop&q=80",
        "description": "City of Lakes, featuring the breathtaking City Palace floating on Lake Pichola, romance, and sunsets."
    },
    {
        "name": "Rishikesh",
        "state": "Uttarakhand",
        "lat": 30.0869,
        "lon": 78.2676,
        "interests": ["adventure", "spiritual", "nature", "yoga", "rafting"],
        "best_season": ["spring", "summer", "winter"],
        "avg_cost": 1500,
        "safety": 92,
        "image": "https://images.unsplash.com/photo-1598970434795-0c54fe7c0648?w=600&auto=format&fit=crop&q=80",
        "description": "Yoga capital of the world on the banks of the emerald Ganges, white-water rafting, and suspension bridges."
    },
    {
        "name": "Andaman Islands",
        "state": "Andaman",
        "lat": 11.6234,
        "lon": 92.7265,
        "interests": ["beach", "adventure", "nature", "scuba", "island"],
        "best_season": ["winter", "spring"],
        "avg_cost": 4200,
        "safety": 86,
        "image": "https://images.unsplash.com/photo-1589308078059-be1415eab4c3?w=600&auto=format&fit=crop&q=80",
        "description": "Pristine white sand beaches, Radhanagar turquoise waters, coral reef scuba diving, and tropical seclusion."
    }
]

def get_realtime_weather(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
        resp = requests.get(url, timeout=3)
        if resp.status_code == 200:
            data = resp.json().get("current", {})
            code = data.get("weather_code", 0)
            
            if code == 0: condition = "Clear Sky ☀️"
            elif code in [1, 2, 3]: condition = "Partly Cloudy ⛅"
            elif code in [45, 48]: condition = "Foggy 🌫️"
            elif code in [51, 53, 55, 61, 63, 65]: condition = "Light Rain 🌧️"
            elif code in [80, 81, 82]: condition = "Rain Showers 🌦️"
            elif code in [95, 96, 99]: condition = "Thunderstorm 🌩️"
            else: condition = "Pleasant Climate 🌤️"
            
            return {
                "temp": round(data.get("temperature_2m", 25), 1),
                "humidity": data.get("relative_humidity_2m", 60),
                "wind": data.get("wind_speed_10m", 10),
                "condition": condition,
                "status": "Live Open-Meteo Weather"
            }
    except Exception:
        pass
    return {"temp": 26.5, "humidity": 65, "wind": 12, "condition": "Sunny ☀️", "status": "Estimated"}

def recommend_destinations(budget, duration, interests, season, api_key=None):
    try:
        budget = float(budget)
        duration = int(duration)
    except Exception:
        budget = 25000
        duration = 5

    key = api_key or GEMINI_API_KEY
    if GEMINI_AVAILABLE and key:
        try:
            return _gemini(budget, duration, interests, season, key)
        except Exception:
            pass
    return _rule(budget, duration, interests, season)

def _rule(budget, duration, interests, season):
    ui = [i.strip().lower() for i in str(interests).split(",") if i.strip()]
    scored = []
    for d in INDIAN_DESTINATIONS:
        s = sum(4 for i in ui if any(i in tag for tag in d["interests"]))
        if season.lower() in d["best_season"]:
            s += 5
        est = d["avg_cost"] * duration
        if est <= budget:
            s += 4
        elif est <= budget * 1.3:
            s += 2
        scored.append((s, d, est))
    
    scored.sort(reverse=True, key=lambda x: x[0])
    
    dests = []
    for _, d, est in scored[:4]:
        w = get_realtime_weather(d["lat"], d["lon"])
        dests.append({
            "name": d["name"],
            "state": d["state"],
            "lat": d["lat"],
            "lon": d["lon"],
            "safety_score": d["safety"],
            "estimated_cost": int(est),
            "image": d["image"],
            "description": d["description"],
            "weather": w,
            "why": f"Great choice for {', '.join(ui) or 'travel'}. Current Weather: {w['temp']}°C ({w['condition']})."
        })
    
    itinerary = _itin([d["name"] for d in dests[:1]], duration, ui)
    total_est = sum(d["estimated_cost"] for d in dests[:2])
    return {
        "destinations": dests,
        "budget_estimate": total_est,
        "itinerary": itinerary,
        "source": "Smart AI Engine + Live Open-Meteo Weather"
    }

def _gemini(budget, duration, interests, season, key):
    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        f"Generate travel recommendations for India. Budget: Rs.{budget}, Duration: {duration} days, "
        f"Interests: {interests}, Season: {season}. "
        "Return STRICT JSON: "
        "{ 'destinations': [ {'name': '...', 'state': '...', 'safety_score': 85, 'estimated_cost': 15000, 'why': '...', 'description': '...'} ], "
        "'budget_estimate': 30000, 'itinerary': ['Day 1: ...', 'Day 2: ...'] }."
    )
    res = model.generate_content(prompt)
    txt = res.text.strip()
    if txt.startswith("```"):
        txt = txt.split("```")[1]
        if txt.startswith("json"):
            txt = txt[4:]
    import json
    parsed = json.loads(txt.strip())
    parsed["source"] = "Gemini AI Live"
    dest_map = {d["name"].lower(): d for d in INDIAN_DESTINATIONS}
    for item in parsed.get("destinations", []):
        matched = dest_map.get(item["name"].lower(), {})
        item["lat"] = matched.get("lat", 20.5937)
        item["lon"] = matched.get("lon", 78.9629)
        item["image"] = matched.get("image", "https://images.unsplash.com/photo-1506461883276-594a12b11cf3?w=600&auto=format&fit=crop&q=80")
        item["weather"] = get_realtime_weather(item["lat"], item["lon"])
    return parsed

def _itin(dests, dur, ui):
    out = []
    dest_name = dests[0] if dests else "Destination"
    activities = ui if ui else ["Sightseeing", "Cultural Exploration", "Local Cuisine", "Relaxation"]
    for day in range(1, dur + 1):
        if day == 1:
            out.append(f"Day {day}: Arrival in {dest_name}, hotel check-in, sunset view & local market stroll.")
        elif day == dur:
            out.append(f"Day {day}: Morning souvenir shopping, checkout, and return journey.")
        else:
            act = activities[(day - 2) % len(activities)].title()
            out.append(f"Day {day}: {act} experience in {dest_name} followed by evening local highlights.")
    return out

CROWD_DATA = {
    "Goa": {"peak_months": [12,1,2], "weekend_factor": 1.4, "base": 65, "lat": 15.2993, "lon": 74.1240},
    "Manali": {"peak_months": [5,6,12], "weekend_factor": 1.5, "base": 60, "lat": 32.2432, "lon": 77.1892},
    "Jaipur": {"peak_months": [11,12,1,2], "weekend_factor": 1.3, "base": 55, "lat": 26.9124, "lon": 75.7873},
    "Kerala Backwaters": {"peak_months": [12,1], "weekend_factor": 1.2, "base": 48, "lat": 9.4981, "lon": 76.3388},
    "Varanasi": {"peak_months": [10,11,3], "weekend_factor": 1.4, "base": 70, "lat": 25.3176, "lon": 82.9739},
    "Udaipur": {"peak_months": [11,12,2], "weekend_factor": 1.3, "base": 50, "lat": 24.5854, "lon": 73.7125},
    "Rishikesh": {"peak_months": [3,4,9,10], "weekend_factor": 1.5, "base": 55, "lat": 30.0869, "lon": 78.2676},
    "Andaman Islands": {"peak_months": [12,1,2], "weekend_factor": 1.3, "base": 42, "lat": 11.6234, "lon": 92.7265}
}

def predict_crowd(dest, date_str):
    try:
        # Handle non-standard or invalid dates safely
        parts = date_str.split("-")
        if len(parts) == 3:
            y, m, d_val = int(parts[0]), int(parts[1]), min(28, int(parts[2]))
            d = datetime(y, m, d_val)
        else:
            d = datetime.now()
    except Exception:
        d = datetime.now()
    
    info = CROWD_DATA.get(dest, {"peak_months": [6], "weekend_factor": 1.3, "base": 50, "lat": 20.5937, "lon": 78.9629})
    s = info["base"]
    if d.month in info["peak_months"]:
        s += 25
    if d.weekday() >= 5:
        s *= info["weekend_factor"]
        
    s = max(10, min(98, int(s)))
    
    if s >= 75:
        lvl, adv = "Very High Density", "Avoid peak hours (10 AM - 4 PM). Pre-book entry tickets online."
        badge = "🔴 Critical"
    elif s >= 55:
        lvl, adv = "Moderate to High", "Expect queues. Pre-book transport and tickets online."
        badge = "🟠 Elevated"
    elif s >= 35:
        lvl, adv = "Normal Flow", "Comfortable crowd levels. Smooth access to major attractions."
        badge = "🟡 Moderate"
    else:
        lvl, adv = "Low Density", "Optimal quiet travel time - minimal waiting lines."
        badge = "🟢 Quiet"
        
    hourly = []
    for h in range(8, 22):
        factor = 0.4 + 0.6 * (1.0 - abs(h - 14) / 7.0)
        hourly.append({"Hour": f"{h:02d}:00", "Density": round(s * factor)})
        
    weather = get_realtime_weather(info["lat"], info["lon"])
    
    return {
        "destination": dest,
        "date": d.strftime("%Y-%m-%d"),
        "score": s,
        "level": lvl,
        "advice": adv,
        "badge": badge,
        "lat": info["lat"],
        "lon": info["lon"],
        "weather": weather,
        "hourly": hourly
    }

SAFETY_FACTORS = {
    "Goa": {"crime": 15, "medical": 10, "transport": 10, "women_safety": 12, "lat": 15.2993, "lon": 74.1240},
    "Manali": {"crime": 8, "medical": 14, "transport": 16, "women_safety": 8, "lat": 32.2432, "lon": 77.1892},
    "Jaipur": {"crime": 20, "medical": 12, "transport": 15, "women_safety": 18, "lat": 26.9124, "lon": 75.7873},
    "Kerala Backwaters": {"crime": 10, "medical": 8, "transport": 10, "women_safety": 9, "lat": 9.4981, "lon": 76.3388},
    "Varanasi": {"crime": 24, "medical": 18, "transport": 22, "women_safety": 25, "lat": 25.3176, "lon": 82.9739},
    "Udaipur": {"crime": 14, "medical": 12, "transport": 12, "women_safety": 14, "lat": 24.5854, "lon": 73.7125},
    "Rishikesh": {"crime": 10, "medical": 10, "transport": 12, "women_safety": 10, "lat": 30.0869, "lon": 78.2676},
    "Andaman Islands": {"crime": 8, "medical": 20, "transport": 15, "women_safety": 10, "lat": 11.6234, "lon": 92.7265}
}

def compute_safety(dest, tod="day", solo=False):
    f = SAFETY_FACTORS.get(dest, {"crime": 18, "medical": 15, "transport": 15, "women_safety": 18, "lat": 20.5937, "lon": 78.9629})
    raw_factors = {k: v for k, v in f.items() if k not in ["lat", "lon"]}
    
    risk = sum(raw_factors.values())
    if tod == "night":
        risk += 18
    if solo:
        risk += raw_factors["women_safety"] // 2
        
    score = max(5, 100 - risk)
    
    if score >= 82:
        rating, color, hex_code = "Safe & Secure", "green", "#10B981"
    elif score >= 65:
        rating, color, hex_code = "Good (Normal Care)", "blue", "#3B82F6"
    elif score >= 45:
        rating, color, hex_code = "Moderate Caution Needed", "orange", "#F59E0B"
    else:
        rating, color, hex_code = "High Vigilance Recommended", "red", "#EF4444"
        
    tips = [
        "Keep digital copies of identity documents & emergency contacts in cloud.",
        "Use verified app-based transit (Ola/Uber) or authorized prepaid taxis.",
        "Save local tourist emergency helpline numbers (1363 / 112)."
    ]
    if tod == "night":
        tips.append("Stick to well-lit commercial thoroughfares; avoid unlit isolated alleys.")
    if solo:
        tips.append("Activate live GPS track sharing with trusted emergency contact.")
        
    weather = get_realtime_weather(f["lat"], f["lon"])
    
    return {
        "score": score,
        "rating": rating,
        "color": color,
        "hex": hex_code,
        "factors": raw_factors,
        "tips": tips,
        "lat": f["lat"],
        "lon": f["lon"],
        "weather": weather
    }

def estimate_budget(dest, days, travelers, style="mid"):
    try:
        days = int(days)
        travelers = int(travelers)
    except Exception:
        days = 5
        travelers = 2

    bs = {"budget": 900, "mid": 2500, "luxury": 6500}.get(style, 2500)
    bf = {"budget": 450, "mid": 1000, "luxury": 2500}.get(style, 1000)
    bt = {"budget": 350, "mid": 850, "luxury": 2200}.get(style, 850)
    ba = {"budget": 350, "mid": 950, "luxury": 2500}.get(style, 950)
    
    dm = {"Goa": 1.15, "Manali": 1.1, "Jaipur": 1.0, "Kerala Backwaters": 1.25,
          "Varanasi": 0.85, "Udaipur": 1.1, "Rishikesh": 0.95, "Andaman Islands": 1.45}.get(dest, 1.0)
          
    stay = bs * days * travelers * dm
    food = bf * days * travelers
    trans = bt * days * travelers
    act = ba * days * travelers
    buf = 0.12 * (stay + food + trans + act)
    total = stay + food + trans + act + buf
    
    return {
        "stay": round(stay),
        "food": round(food),
        "transport": round(trans),
        "activities": round(act),
        "buffer": round(buf),
        "total": round(total),
        "per_person": round(total / max(1, travelers))
    }

def travel_guardian_report(dest, date_str, tod="day", solo=False):
    crowd = predict_crowd(dest, date_str)
    safety = compute_safety(dest, tod, solo)
    
    alerts = []
    if crowd["score"] >= 75:
        alerts.append(f"⚠️ HIGH CROWD ALERT: {dest} crowd score is {crowd['score']}/100. {crowd['advice']}")
    if safety["score"] < 50:
        alerts.append(f"🚨 SAFETY NOTICE: Safety index is low ({safety['score']}/100). Exercise extra caution.")
    if tod == "night":
        alerts.append("🌙 NIGHT TRAIL: Avoid dark remote zones; travel in group or use official taxi.")
    if not alerts:
        alerts.append(f"✅ ALL CLEAR: Weather ({safety['weather']['temp']}°C), safety & crowd metrics are optimal!")
        
    plan_b = None
    if crowd["score"] >= 75 or safety["score"] < 50:
        alts = [d["name"] for d in INDIAN_DESTINATIONS if d["name"] != dest][:3]
        plan_b = f"Suggested Peaceful Alternatives: {', '.join(alts)}"
        
    return {
        "destination": dest,
        "crowd": crowd,
        "safety": safety,
        "alerts": alerts,
        "plan_b": plan_b
    }

def assistant_reply(question, ctx="", api_key=None):
    key = api_key or GEMINI_API_KEY
    if GEMINI_AVAILABLE and key:
        try:
            m = genai.GenerativeModel("gemini-1.5-flash")
            prompt = (
                f"You are TravelGuardian AI, an expert, polite, and protective AI travel assistant for tourists in India. "
                f"Context: {ctx}. User question: '{question}'. "
                "Provide a helpful, precise, and safe answer."
            )
            return m.generate_content(prompt).text
        except Exception:
            pass
            
    q = str(question).lower()
    if "food" in q or "eat" in q:
        return "Culinary Guidance: Eat freshly cooked meals at busy local spots. Stick to sealed mineral water bottles."
    if "safe" in q or "night" in q or "female" in q:
        return "Safety Advisory: Share your live GPS location. Keep Emergency Numbers saved: 112 (Universal), 1091 (Women Helpline), 1363 (Tourist Line)."
    if "budget" in q or "cheap" in q:
        return "Savings Advice: Travel via IRCTC Express trains. Stay in certified homestays or hostels."
    if "best time" in q or "season" in q:
        return "Optimal Windows: October to March is ideal for Goa, Rajasthan, Kerala & Varanasi."
    return "TravelGuardian Assistant: I am here to protect and guide your journey across India! Ask me about destinations, emergency contacts, local customs, budget planning, or safety scores."
