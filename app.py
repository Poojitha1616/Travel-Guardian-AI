"""
TravelGuardian AI - Advanced Smart Tourism & Tourist Safety Platform
Built with Streamlit, Plotly, Folium, and Web Speech API.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta, datetime
import json, base64

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import folium
from streamlit_folium import st_folium

import db
import ai_engine as ai

# Page configuration
st.set_page_config(
    page_title="TravelGuardian AI | Smart Tourism & Safety",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database
db.init_db()

# Session State Initialization
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "Login"
if "reset_token" not in st.session_state:
    st.session_state.reset_token = None
if "gemini_key" not in st.session_state:
    st.session_state.gemini_key = ""
if "active_call" not in st.session_state:
    st.session_state.active_call = False

# Global CSS with Glassmorphism and Modern Aesthetics
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

h1, h2, h3, h4, .stSubheader {
    font-family: 'Outfit', sans-serif !important;
}

/* Background gradient */
.stApp {
    background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #0F172A 100%);
    color: #F8FAFC;
}

/* Hide default header */
header[data-testid="stHeader"] {
    background: rgba(15, 23, 42, 0.8) !important;
    backdrop-filter: blur(12px);
}

/* Main Header Card */
.hero-banner {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(168, 85, 247, 0.25) 100%);
    border: 1px solid rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 1.8rem 2.2rem;
    margin-bottom: 2rem;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    position: relative;
    overflow: hidden;
}

.hero-banner::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(129, 140, 248, 0.3) 0%, rgba(0,0,0,0) 70%);
    pointer-events: none;
}

.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #FFFFFF 0%, #C7D2FE 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.hero-subtitle {
    color: #94A3B8;
    font-size: 1.05rem;
    margin-top: 0.3rem;
    margin-bottom: 0;
}

/* Glassmorphic Metric Cards */
.glass-card {
    background: rgba(30, 41, 59, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(16px);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    margin-bottom: 1.2rem;
}

.glass-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 35px rgba(99, 102, 241, 0.2);
    border-color: rgba(168, 85, 247, 0.3);
}

.metric-val {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #818CF8, #C084FC);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.metric-lbl {
    color: #94A3B8;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Alert Boxes */
.alert-card-warning {
    background: rgba(245, 158, 11, 0.15);
    border-left: 5px solid #F59E0B;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: #FDE68A;
    margin-bottom: 1rem;
}

.alert-card-danger {
    background: rgba(239, 68, 68, 0.18);
    border-left: 5px solid #EF4444;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: #FCA5A5;
    margin-bottom: 1rem;
}

.alert-card-success {
    background: rgba(16, 185, 129, 0.15);
    border-left: 5px solid #10B981;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: #A7F3D0;
    margin-bottom: 1rem;
}

/* Buttons */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
}

.stButton > button[kind="primary"]:hover {
    transform: scale(1.02) !important;
    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6) !important;
}

/* Custom Call Modal Container */
.call-modal {
    background: radial-gradient(circle at center, #1E1B4B 0%, #0F172A 100%);
    border: 2px solid #818CF8;
    border-radius: 24px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 0 50px rgba(99, 102, 241, 0.5);
}

.pulse-ring {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    background: #6366F1;
    box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.7);
    animation: pulse 1.6s infinite;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1.5rem auto;
    font-size: 2.5rem;
}

@keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.7); }
    70% { transform: scale(1.08); box-shadow: 0 0 0 25px rgba(99, 102, 241, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); }
}

/* Boarding Pass Badge */
.boarding-pass {
    background: linear-gradient(135deg, #1E293B, #0F172A);
    border: 1px dashed rgba(255, 255, 255, 0.2);
    border-radius: 16px;
    padding: 1.5rem;
    position: relative;
}
</style>
""", unsafe_allow_html=True)

# Navigation helper
def logout():
    st.session_state.user = None
    st.session_state.page = "Login"

# Top Navigation Bar Banner
def render_header():
    u = st.session_state.user
    name_str = f"Welcome, {u['name']}" if u else "TravelGuardian AI"
    role_badge = f" <span style='background:#6366F1;padding:3px 10px;border-radius:12px;font-size:0.75rem;'>{u['role']}</span>" if u else ""
    
    st.markdown(f"""
    <div class="hero-banner">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div class="hero-title">🛡️ TravelGuardian AI{role_badge}</div>
                <div class="hero-subtitle">Smart Tourist Safety & AI Recommendation Platform</div>
            </div>
            <div style="text-align:right;">
                <div style="font-weight:700; font-size:1.1rem; color:#E2E8F0;">{name_str}</div>
                <div style="font-size:0.85rem; color:#10B981;">🟢 Live Emergency Sentinel Active</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------- PAGE HANDLERS -----------------

def page_login():
    st.markdown("<h2 style='text-align:center;'>🔐 Sign In to TravelGuardian</h2>", unsafe_allow_html=True)
    st.caption("Access personalized recommendations, wallet, emergency SOS, and live AI assistant.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        email = st.text_input("Email Address", value="user@tg.ai", key="le")
        password = st.text_input("Password", value="user123", type="password", key="lp")
        
        c_sub1, c_sub2 = st.columns(2)
        with c_sub1:
            if st.button("Log In", type="primary", use_container_width=True):
                u, err = db.login(email, password)
                if err:
                    st.error(err)
                else:
                    st.session_state.user = u
                    st.session_state.page = "Home"
                    st.rerun()
        with c_sub2:
            if st.button("Quick Admin Demo", use_container_width=True):
                u, err = db.login("admin@tg.ai", "admin123")
                if not err:
                    st.session_state.user = u
                    st.session_state.page = "Home"
                    st.rerun()
        
        st.markdown("---")
        st.markdown("""
        <div style='font-size:0.85rem; color:#94A3B8; text-align:center;'>
            <b>Demo Credentials:</b><br>
            👤 User: <code>user@tg.ai</code> / <code>user123</code><br>
            👑 Admin: <code>admin@tg.ai</code> / <code>admin123</code>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def page_signup():
    st.markdown("<h2 style='text-align:center;'>✨ Create Your TravelGuardian Account</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        n = st.text_input("Full Name", key="sn")
        e = st.text_input("Email Address", key="se")
        p = st.text_input("Password (min 6 characters)", type="password", key="sp")
        
        if st.button("Create Free Account", type="primary", use_container_width=True):
            if not n or not e or len(p) < 6:
                st.error("Please fill in all details with a password of at least 6 characters.")
            else:
                u, err = db.signup(n, e, p)
                if err:
                    st.error(err)
                else:
                    st.session_state.user = u
                    st.session_state.page = "Home"
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def page_forgot():
    st.markdown("<h2 style='text-align:center;'>🔑 Password Recovery</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        e = st.text_input("Registered Email", key="fe")
        if st.button("Generate Reset Token", type="primary", use_container_width=True):
            t = db.create_reset_token(e)
            if t:
                st.success(f"Security token generated: {t}")
                st.session_state.reset_token = t
            else:
                st.info("If this email exists, a reset token has been issued.")
                
        if st.session_state.reset_token:
            st.markdown("---")
            np_ = st.text_input("Enter New Password", type="password", key="fp")
            if st.button("Set New Password", use_container_width=True):
                ok, msg = db.reset_password(st.session_state.reset_token, np_)
                if ok:
                    st.success("Password updated successfully! You can now login.")
                    st.session_state.reset_token = None
                else:
                    st.error(msg)
        st.markdown('</div>', unsafe_allow_html=True)

def page_home():
    u = st.session_state.user
    w = db.get_wallet(u["id"])
    bs = db.get_bookings(u["id"])
    active_b = len([b for b in bs if b["status"] == "CONFIRMED"])
    
    st.markdown(f"### 👋 Welcome back, {u['name']}!")
    
    # Hero Metric Cards Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-lbl">Demo Wallet</div>
            <div class="metric-val">₹{w['balance']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-lbl">Total Trips</div>
            <div class="metric-val">{len(bs)}</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-lbl">Active Bookings</div>
            <div class="metric-val" style="background: linear-gradient(90deg,#34D399,#10B981);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{active_b}</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-lbl">Guardian Status</div>
            <div class="metric-val" style="font-size:1.5rem; color:#10B981;">🛡️ 100% Safe</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("### ⚡ Quick Navigation Center")
    
    q1, q2, q3, q4 = st.columns(4)
    with q1:
        if st.button("✈️ AI Trip Planner", use_container_width=True, type="primary"):
            st.session_state.page = "AI Recommend"
            st.rerun()
    with q2:
        if st.button("📊 Crowd Radar", use_container_width=True):
            st.session_state.page = "Crowd"
            st.rerun()
    with q3:
        if st.button("📞 AI Voice Call", use_container_width=True):
            st.session_state.page = "AI Voice Call"
            st.rerun()
    with q4:
        if st.button("🚨 Emergency SOS", use_container_width=True):
            st.session_state.page = "SOS"
            st.rerun()
            
    st.markdown("### 🌟 Popular Indian Destinations Spotlight")
    cols = st.columns(4)
    for idx, d in enumerate(ai.INDIAN_DESTINATIONS[:4]):
        with cols[idx]:
            st.markdown(f"""
            <div class="glass-card" style="padding:0; overflow:hidden;">
                <img src="{d['image']}" style="width:100%; height:140px; object-fit:cover;">
                <div style="padding:1rem;">
                    <h4 style="margin:0; font-size:1.1rem; color:#F8FAFC;">{d['name']}</h4>
                    <p style="font-size:0.8rem; color:#94A3B8; margin:0.3rem 0;">{d['state']}</p>
                    <div style="display:flex; justify-content:space-between; margin-top:0.8rem; font-size:0.85rem;">
                        <span style="color:#818CF8; font-weight:700;">₹{d['avg_cost']}/day</span>
                        <span style="color:#10B981; font-weight:700;">🛡️ {d['safety']}/100</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def page_ai_recommend():
    st.markdown("## 🧭 AI Tourist Destination & Itinerary Generator")
    st.caption("Smart destination matching based on budget, travel preferences, season, and safety scores.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Travel Preferences")
        budget = st.number_input("Total Budget (₹)", min_value=2000, value=25000, step=1000)
        duration = st.slider("Duration (Days)", 2, 20, 5)
        season = st.selectbox("Travel Season", ["Winter", "Summer", "Monsoon", "Spring"])
        interests = st.text_input("Interests & Vibes", value="beach, food, culture, adventure")
        
        run_btn = st.button("🚀 Generate AI Recommendations", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        if run_btn:
            with st.spinner("AI is analyzing weather, crowd index, and budget fit..."):
                r = ai.recommend_destinations(budget, duration, interests, season, st.session_state.gemini_key)
            st.session_state.rec_result = r
            
        if "rec_result" in st.session_state:
            r = st.session_state.rec_result
            st.markdown(f"<div class='alert-card-success'>✨ Intelligence Engine: <b>{r.get('source','AI')}</b></div>", unsafe_allow_html=True)
            
            dests = r.get("destinations", [])
            for d in dests:
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display:flex; gap:1.5rem; align-items:center;">
                        <img src="{d.get('image','')}" style="width:120px; height:100px; border-radius:12px; object-fit:cover;">
                        <div style="flex:1;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <h3 style="margin:0; color:#F8FAFC;">{d['name']} <span style="font-size:0.9rem; color:#94A3B8; font-weight:400;">({d.get('state','')})</span></h3>
                                <span style="background:rgba(16, 185, 129, 0.2); color:#34D399; padding:4px 12px; border-radius:12px; font-weight:700;">Safety: {d.get('safety_score','?')}/100</span>
                            </div>
                            <p style="font-size:0.9rem; color:#CBD5E1; margin:0.4rem 0;">{d.get('why','')}</p>
                            <div style="font-size:0.85rem; color:#818CF8; font-weight:600;">Est. Cost for {duration} Days: ₹{d.get('estimated_cost',0):,}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("### 📝 Custom Generated Day-by-Day Itinerary")
            for day in r.get("itinerary", []):
                st.markdown(f"• {day}")

def page_crowd():
    st.markdown("## 📊 AI Real-Time Crowd Density Prediction")
    st.caption("Forecast tourist density, peak congestion hours, and optimal visiting schedules.")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        dest = st.selectbox("Select Destination", list(ai.CROWD_DATA.keys()))
        dt = st.date_input("Target Visit Date", value=date.today() + timedelta(days=5))
        predict_btn = st.button("Analyze Density", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        r = ai.predict_crowd(dest, dt.isoformat())
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div class="glass-card">
                <div class="metric-lbl">Density Index</div>
                <div class="metric-val">{r['score']}/100</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="glass-card">
                <div class="metric-lbl">Status</div>
                <div class="metric-val" style="font-size:1.4rem;">{r['badge']}</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="glass-card">
                <div class="metric-lbl">Congestion Level</div>
                <div class="metric-val" style="font-size:1.4rem; color:#F59E0B;">{r['level']}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown(f"<div class='alert-card-warning'>💡 <b>Guardian Travel Advisory:</b> {r['advice']}</div>", unsafe_allow_html=True)
        
        st.markdown("### 📈 Projected Hourly Crowd Profile (8:00 AM - 10:00 PM)")
        df_hourly = pd.DataFrame(r["hourly"])
        fig = px.area(
            df_hourly, x="Hour", y="Density",
            title=f"Expected Density Curve for {dest} on {r['date']}",
            color_discrete_sequence=["#818CF8"]
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#F8FAFC"
        )
        st.plotly_chart(fig, use_container_width=True)

def page_safety():
    st.markdown("## 🛡️ Tourist Safety Intelligence & Risk Scanner")
    st.caption("Deep multi-dimensional safety matrix covering crime, healthcare, night travel, and female traveler scores.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        dest = st.selectbox("Destination", list(ai.SAFETY_FACTORS.keys()))
    with c2:
        tod = st.selectbox("Time of Day", ["day", "night"])
    with c3:
        solo = st.checkbox("Solo Female Traveler Mode", value=True)
        
    r = ai.compute_safety(dest, tod, solo)
    
    col_left, col_right = st.columns([1, 1])
    with col_left:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding:2rem;">
            <div class="metric-lbl">Comprehensive Safety Index</div>
            <div style="font-size:4rem; font-weight:800; color:{r['hex']};">{r['score']}/100</div>
            <div style="font-size:1.3rem; font-weight:700; color:{r['hex']};">{r['rating']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📋 Essential Safety Recommendations")
        for tip in r["tips"]:
            st.markdown(f"• {tip}")
            
    with col_right:
        st.markdown("### 🎯 Risk Factor Breakdown")
        df_factors = pd.DataFrame(list(r["factors"].items()), columns=["Factor", "Risk Level"])
        fig = px.bar(
            df_factors, x="Factor", y="Risk Level",
            color="Risk Level", color_continuous_scale="Reds",
            title=f"Threat Multipliers for {dest}"
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#F8FAFC"
        )
        st.plotly_chart(fig, use_container_width=True)

def page_budget():
    st.markdown("## 💰 Smart Travel Budget & Cost Estimator")
    st.caption("Accurate expense forecasting across stay, food, transport, activities, and emergency buffer.")
    
    c1, c2 = st.columns(2)
    with c1:
        dest = st.selectbox("Destination", list(ai.CROWD_DATA.keys()), key="b_dest")
        days = st.slider("Duration (Days)", 1, 30, 5, key="b_days")
    with c2:
        tr = st.slider("Travelers Count", 1, 10, 2, key="b_tr")
        style = st.selectbox("Travel Comfort Tier", ["budget", "mid", "luxury"], index=1)
        
    b = ai.estimate_budget(dest, days, tr, style)
    
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-lbl">Total Estimated Trip Cost</div>
            <div class="metric-val">₹{b['total']:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-lbl">Cost Per Person</div>
            <div class="metric-val" style="color:#34D399;">₹{b['per_person']:,}</div>
        </div>
        """, unsafe_allow_html=True)
        
    df_budget = pd.DataFrame({
        "Category": ["Stay/Hotel", "Dining & Food", "Local Transit", "Sightseeing/Activities", "Emergency Buffer"],
        "Amount (₹)": [b["stay"], b["food"], b["transport"], b["activities"], b["buffer"]]
    })
    
    c_pie, c_bar = st.columns(2)
    with c_pie:
        fig_pie = px.pie(df_budget, names="Category", values="Amount (₹)", title="Expense Distribution", hole=0.4)
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#F8FAFC")
        st.plotly_chart(fig_pie, use_container_width=True)
    with c_bar:
        fig_bar = px.bar(df_budget, x="Category", y="Amount (₹)", color="Category", title="Category Comparison")
        fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#F8FAFC")
        st.plotly_chart(fig_bar, use_container_width=True)

def page_guardian():
    st.markdown("## 🛡️ AI Travel Guardian Real-Time Radar")
    st.caption("360-degree risk assessment, contingency plan recommendation, and safety advisory.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        dest = st.selectbox("Destination", list(ai.CROWD_DATA.keys()), key="gd")
    with c2:
        dt = st.date_input("Travel Date", value=date.today()+timedelta(days=3), key="gdt")
    with c3:
        tod = st.selectbox("Time Window", ["day", "night"], key="gt")
        
    solo = st.checkbox("Solo Female Traveler Mode", value=True, key="gs")
    
    r = ai.travel_guardian_report(dest, dt.isoformat(), tod, solo)
    
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-lbl">Crowd Density Index</div>
            <div class="metric-val">{r['crowd']['score']}/100 ({r['crowd']['level']})</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-lbl">Safety Security Index</div>
            <div class="metric-val" style="color:{r['safety']['hex']}">{r['safety']['score']}/100 ({r['safety']['rating']})</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("### ⚠️ Active Sentinel Advisories")
    for alert in r["alerts"]:
        if "WARNING" in alert or "ALERT" in alert:
            st.markdown(f"<div class='alert-card-danger'>{alert}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='alert-card-success'>{alert}</div>", unsafe_allow_html=True)
            
    if r["plan_b"]:
        st.markdown(f"<div class='alert-card-warning'>🔄 <b>Contingency Plan B:</b> {r['plan_b']}</div>", unsafe_allow_html=True)

# ----------------- AI VOICE CALL SIMULATION PAGE -----------------
def page_voice_call():
    st.markdown("## 📞 AI Travel Guardian Live Voice Call")
    st.caption("Interactive voice assistance powered by Web Speech API. Ask questions or listen to audio safety briefings.")
    
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.markdown("""
        <div class="call-modal">
            <div class="pulse-ring">🎙️</div>
            <h2 style="margin:0; color:#FFFFFF;">AI Guardian 24/7 Voice Hotline</h2>
            <p style="color:#A5B4FC; font-weight:600; margin-top:0.4rem;">Connected · Encrypted Safety Line</p>
            <div style="font-family:monospace; font-size:1.8rem; color:#34D399; margin:1rem 0;">00:42 SEC</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.markdown("#### 🗣️ Speak or Ask AI Guardian")
        
        user_speech = st.text_input("Type your question or query to hear voice response:", value="Is Goa safe for solo female travelers at night?")
        
        voice_rate = st.slider("Voice Speed Rate", 0.7, 1.5, 1.0, 0.1)
        
        if st.button("🔊 Play AI Voice Response", type="primary", use_container_width=True):
            reply_text = ai.assistant_reply(user_speech, api_key=st.session_state.gemini_key)
            
            # Clean text for speech output
            clean_reply = reply_text.replace("*", "").replace("#", "").replace("\n", " ")
            
            st.success(f"**AI Response:** {reply_text}")
            
            # HTML5 Web Speech Synthesis API snippet
            html_code = f"""
            <script>
                var msg = new SpeechSynthesisUtterance({json.dumps(clean_reply)});
                msg.rate = {voice_rate};
                msg.pitch = 1.0;
                window.speechSynthesis.speak(msg);
            </script>
            <div style="padding:10px; background:rgba(99,102,241,0.2); border-radius:8px; text-align:center; color:#A5B4FC;">
                🔊 Audio is playing through your browser speakers...
            </div>
            """
            st.components.v1.html(html_code, height=60)
            
    with col_side:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### ⚡ Quick Voice Triggers")
        if st.button("📢 Play Safety Briefing"):
            briefing = "Welcome to TravelGuardian. Keep emergency number 1 1 2 saved. Always share live location."
            html_code = f"<script>var m=new SpeechSynthesisUtterance({json.dumps(briefing)});window.speechSynthesis.speak(m);</script>"
            st.components.v1.html(html_code, height=40)
            
        if st.button("🚨 Trigger Audio Emergency Alarm"):
            siren_code = """
            <script>
                var ctx = new (window.AudioContext || window.webkitAudioContext)();
                var osc = ctx.createOscillator();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(800, ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(400, ctx.currentTime + 0.5);
                osc.connect(ctx.destination);
                osc.start();
                osc.stop(ctx.currentTime + 1.0);
            </script>
            <div style="color:#EF4444; font-weight:700;">🚨 Siren Sounded!</div>
            """
            st.components.v1.html(siren_code, height=40)
        st.markdown('</div>', unsafe_allow_html=True)

def page_booking():
    u = st.session_state.user
    st.markdown("## 🎫 Smart Ticket Booking & Pass Generator")
    st.caption("Book flights, trains, buses, or hotels instantly using your Demo Wallet.")
    
    t1, t2 = st.tabs(["✈️ Create New Booking", "📜 My Bookings & Boarding Passes"])
    
    with t1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            btype = st.selectbox("Transport / Stay Type", ["FLIGHT", "TRAIN", "BUS", "HOTEL"])
            fc = st.text_input("Origin / Departure City", value="New Delhi", key="bf")
        with c2:
            tc = st.text_input("Destination City", value="Goa", key="bt2")
            bd = st.date_input("Travel Date", value=date.today()+timedelta(days=7))
        
        amt = st.number_input("Ticket Fare (₹)", min_value=200, value=4500, step=100)
        
        if st.button("💳 Confirm Booking & Deduct Wallet", type="primary", use_container_width=True):
            b_res, err = db.create_booking(u["id"], btype, fc, tc, bd.isoformat(), amt)
            if err:
                st.error(f"Booking Failed: {err}")
            else:
                st.success(f"🎉 {btype} Booking Confirmed! Ticket ID: {b_res['id'][:8]}")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with t2:
        bs = db.get_bookings(u["id"])
        if not bs:
            st.info("No bookings registered yet.")
        else:
            for b in bs:
                st.markdown(f"""
                <div class="boarding-pass" style="margin-bottom:1.2rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span style="background:#6366F1; color:#FFF; padding:4px 10px; border-radius:8px; font-weight:700; font-size:0.8rem;">{b['type']}</span>
                            <h3 style="margin:0.4rem 0 0 0; color:#F8FAFC;">{b['from_city']} ➔ {b['to_city']}</h3>
                            <p style="color:#94A3B8; font-size:0.85rem; margin:0.2rem 0;">Date: {b['date']} | Fare: ₹{b['amount']:,}</p>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-weight:700; color:{'#10B981' if b['status']=='CONFIRMED' else '#EF4444'}; font-size:1.1rem;">{b['status']}</div>
                            <p style="font-size:0.75rem; color:#64748B;">PNR: TG-{b['id'][:8].upper()}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if b["status"] == "CONFIRMED":
                    if st.button("Cancel & Request Refund", key=f"c_{b['id']}"):
                        res, err = db.cancel_booking(u["id"], b["id"])
                        if err:
                            st.error(err)
                        else:
                            st.success(f"Cancelled. ₹{res['refund']} credited back to your wallet (Cancellation Fee: ₹{res['fee']}).")
                            st.rerun()

def page_wallet():
    u = st.session_state.user
    w = db.get_wallet(u["id"])
    
    st.markdown("## 💳 Digital Demo Wallet")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-lbl">Available Wallet Balance</div>
            <div class="metric-val" style="font-size:3rem; color:#34D399;">₹{w['balance']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### ➕ Quick Top-Up Wallet")
        amt = st.number_input("Add Amount (₹)", min_value=100, value=2000, step=500)
        if st.button("Add Funds to Wallet", type="primary", use_container_width=True):
            db.credit(u["id"], amt, "Top-up via Demo UPI")
            st.success(f"₹{amt} added successfully!")
            st.rerun()
            
    with col2:
        st.markdown("### 📜 Transaction Ledger")
        txs = db.get_transactions(u["id"])
        if not txs:
            st.info("No transaction history available.")
        else:
            df_tx = pd.DataFrame(txs)[["created_at", "type", "description", "amount"]]
            df_tx.columns = ["Date & Time", "Type", "Description", "Amount (₹)"]
            st.dataframe(df_tx, use_container_width=True, hide_index=True)

def page_assistant():
    st.markdown("## 🤖 AI Travel Assistant Chat")
    st.caption("Ask questions about local cuisine, travel safety, optimal seasons, or transport options.")
    
    if "chat" not in st.session_state:
        st.session_state.chat = [
            ("assistant", "Hello! I am your TravelGuardian AI assistant. How can I assist your trip today?")
        ]
        
    for role, msg in st.session_state.chat:
        with st.chat_message(role):
            st.write(msg)
            
    q = st.chat_input("Ask about safety tips, best places to visit, emergency numbers...")
    if q:
        st.session_state.chat.append(("user", q))
        with st.chat_message("user"):
            st.write(q)
        with st.chat_message("assistant"):
            with st.spinner("AI is thinking..."):
                r = ai.assistant_reply(q, api_key=st.session_state.gemini_key)
            st.write(r)
        st.session_state.chat.append(("assistant", r))

def page_sos():
    st.markdown("## 🚨 Emergency SOS & Live GPS Radar")
    st.error("IN IMMEDIATE DANGER? Call Universal Emergency **112** (India) or Police **100** immediately!")
    
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📍 Current GPS Coordinates")
        lat = st.number_input("Latitude", value=28.6139, format="%.4f")
        lon = st.number_input("Longitude", value=77.2090, format="%.4f")
        
        google_maps_url = f"https://www.google.com/maps?q={lat},{lon}"
        st.link_button("🌐 Open Precise Location in Google Maps", google_maps_url, use_container_width=True)
        
        whatsapp_msg = f"EMERGENCY ALERT! I need immediate help. My current GPS Location: {google_maps_url}"
        wa_url = f"https://api.whatsapp.com/send?text={whatsapp_msg}"
        st.link_button("📲 Broadcast Distress via WhatsApp", wa_url, type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📞 National Helplines")
        df_sos = pd.DataFrame({
            "Service": ["Police Emergency", "Ambulance Medical", "Fire Brigade", "Women Helpline", "National Tourist Line"],
            "Number": ["100 / 112", "108", "101", "1091", "1363"]
        })
        st.table(df_sos)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("### 🗺️ Live Emergency Interactive Map")
    m = folium.Map(location=[lat, lon], zoom_start=13, tiles="OpenStreetMap")
    folium.Marker([lat, lon], popup="Your Current Location", icon=folium.Icon(color="red", icon="user")).add_to(m)
    folium.Marker([lat + 0.01, lon + 0.01], popup="City Hospital", icon=folium.Icon(color="green", icon="plus")).add_to(m)
    folium.Marker([lat - 0.01, lon - 0.01], popup="Central Police Station", icon=folium.Icon(color="blue", icon="shield")).add_to(m)
    st_folium(m, width="100%", height=350)

def page_profile():
    u = st.session_state.user
    st.markdown("## 👤 User Profile")
    st.markdown(f"""
    <div class="glass-card">
        <h3>{u['name']}</h3>
        <p><b>Email:</b> {u['email']}</p>
        <p><b>Role Tier:</b> {u['role']}</p>
        <p><b>Account Created:</b> {u['created_at'][:10]}</p>
    </div>
    """, unsafe_allow_html=True)

def page_admin():
    if st.session_state.user["role"] != "ADMIN":
        st.error("Admin access required."); return
    
    st.markdown("## 👑 Admin Control Center")
    a = db.admin_analytics()
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Users", a["users"])
    m2.metric("Total Bookings", a["bookings"])
    m3.metric("Cancellations", a["cancelled"])
    m4.metric("Total Wallet Float", f"₹{a['wallet_total']:,.0f}")
    
    t1, t2 = st.tabs(["👥 User Directory", "🎫 Booking Audit Trail"])
    with t1:
        st.dataframe(pd.DataFrame(db.admin_all_users()), use_container_width=True)
    with t2:
        st.dataframe(pd.DataFrame(db.admin_all_bookings()), use_container_width=True)

# ----------------- SIDEBAR CONFIG -----------------
with st.sidebar:
    st.markdown("### 🛡️ TravelGuardian AI")
    
    if not st.session_state.user:
        ap = ["Login", "Signup", "Forgot Password"]
        idx = ap.index(st.session_state.page) if st.session_state.page in ap else 0
        st.session_state.page = st.radio("Navigation", ap, index=idx)
    else:
        pages = [
            "Home", "AI Recommend", "Crowd", "Safety", "Budget",
            "AI Guardian", "AI Voice Call", "Booking", "Wallet",
            "Assistant", "SOS", "Profile"
        ]
        if st.session_state.user["role"] == "ADMIN":
            pages.append("Admin")
            
        idx = pages.index(st.session_state.page) if st.session_state.page in pages else 0
        st.session_state.page = st.radio("Navigation Menu", pages, index=idx)
        
        st.markdown("---")
        st.caption(f"Logged in as: **{st.session_state.user['name']}**")
        
        # Optional Gemini API Key input
        st.markdown("#### 🔑 Gemini API Key (Optional)")
        g_key = st.text_input("Gemini API Key", value=st.session_state.gemini_key, type="password", key="g_input")
        if g_key != st.session_state.gemini_key:
            st.session_state.gemini_key = g_key
            
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()

# Render Header & Active Page
render_header()

PAGES = {
    "Login": page_login,
    "Signup": page_signup,
    "Forgot Password": page_forgot,
    "Home": page_home,
    "AI Recommend": page_ai_recommend,
    "Crowd": page_crowd,
    "Safety": page_safety,
    "Budget": page_budget,
    "AI Guardian": page_guardian,
    "AI Voice Call": page_voice_call,
    "Booking": page_booking,
    "Wallet": page_wallet,
    "Assistant": page_assistant,
    "SOS": page_sos,
    "Profile": page_profile,
    "Admin": page_admin
}

if st.session_state.user is None and st.session_state.page not in ["Login", "Signup", "Forgot Password"]:
    st.session_state.page = "Login"

PAGES[st.session_state.page]()
