import streamlit as st
import pandas as pd
import hashlib

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="OYO Clone | Book Rooms Fast", layout="wide", initial_sidebar_state="expanded")

# --- 2. CUSTOM CSS FOR OYO LOOK & FEEL ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    .property-card {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: white;
        transition: 0.3s;
    }
    .price-tag { color: #d32f2f; font-size: 24px; font-weight: bold; }
    .rating-badge {
        background-color: #388e3c;
        color: white;
        padding: 4px 8px;
        border-radius: 5px;
        font-size: 14px;
    }
    .promo-banner {
        background: linear-gradient(90deg, #ff416c, #ff4b2b);
        color: white;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AUTHENTICATION & SESSION LOGIC ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = "Guest"

def check_login(email, password):
    # Simple Hash for security
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    # Mock Data: password is 'admin123'
    if email == "admin@oyo.com" and hashed_pw == hashlib.sha256("admin123".encode()).hexdigest():
        st.session_state.logged_in = True
        st.session_state.user_role = "Guest"
        return True
    return False

# --- 4. SIDEBAR: AUTH & FILTERS ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/1/19/OYO_Rooms_Logo.svg", width=100)
    
    if not st.session_state.logged_in:
        st.subheader("🔑 Login to Book")
        email = st.text_input("Email", placeholder="admin@oyo.com")
        pw = st.text_input("Password", type="password", placeholder="admin123")
        if st.button("Login"):
            if check_login(email, pw):
                st.success("Logged in!")
                st.rerun()
            else:
                st.error("Invalid credentials")
        st.info("Tip: Use admin@oyo.com / admin123")
    else:
        st.subheader(f"👋 Welcome, {st.session_state.user_role}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
        
        st.divider()
        st.subheader("🔍 Filters")
        price_range = st.sidebar.slider("Price (₹)", 500, 5000, (1000, 3000))
        room_type = st.sidebar.multiselect("Room Type", ["Townhouse", "Flagship", "Silver Key"], default=["Townhouse"])

# --- 5. MAIN CONTENT ---
if not st.session_state.logged_in:
    st.markdown("## 🏨 Welcome to the OYO Clone")
    st.image("https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=80")
    st.warning("Please login from the sidebar to search for hotels and make a booking.")
    st.stop()

# Banner for logged-in users
st.markdown('<div class="promo-banner">🎉 50% OFF on your first booking with OYO Welcome!</div>', unsafe_allow_html=True)

# Mock Hotel Data
properties = [
    {"id": 1, "name": "Super OYO Townhouse 124", "loc": "Sector 45, Gurgaon", "price": 1499, "old": 3200, "rate": 4.3, "lat": 28.4595, "lon": 77.0266, "img": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400"},
    {"id": 2, "name": "OYO Flagship 83445 Premium", "loc": "DLF Phase 3, Gurgaon", "price": 999, "old": 2500, "rate": 4.1, "lat": 28.4900, "lon": 77.0800, "img": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=400"},
    {"id": 3, "name": "Silver Key Executive Stays", "loc": "Golf Course Rd, Gurgaon", "price": 2499, "old": 5000, "rate": 4.7, "lat": 28.4400, "lon": 77.0900, "img": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400"}
]

# Filtering Logic
filtered_props = [p for p in properties if price_range[0] <= p["price"] <= price_range[1]]

# Display Layout
col_list, col_map = st.columns([1.5, 1])

with col_list:
    st.subheader(f"Showing {len(filtered_props)} properties")
    for prop in filtered_props:
        with st.container():
            c1, c2 = st.columns([1, 2])
            with c1:
                st.image(prop["img"], use_container_width=True)
            with c2:
                st.markdown(f"### {prop['name']}")
                st.caption(f"📍 {prop['loc']}")
                st.markdown(f"<span class='rating-badge'>{prop['rate']} ★</span>", unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div style="margin-top:10px;">
                        <span class="price-tag">₹{prop['price']}</span>
                        <span style="text-decoration: line-through; color: gray; margin-left: 10px;">₹{prop['old']}</span>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Book Now", key=f"book_{prop['id']}"):
                    st.success(f"✅ Booking initiated for {prop['name']}!")
                    st.balloons()
            st.divider()

with col_map:
    st.subheader("Map View")
    if filtered_props:
        df = pd.DataFrame(filtered_props)
        st.map(df[['lat', 'lon']])
    else:
        st.write("No properties found in this price range.")
