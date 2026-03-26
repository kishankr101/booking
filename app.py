import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Room Booking App", layout="wide")

# 1. FIXED: Corrected the parameter name to 'unsafe_allow_html'
st.markdown("""
    <style>
    .property-card {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 25px;
        background-color: #ffffff;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .price-tag {
        color: #d32f2f;
        font-size: 24px;
        font-weight: bold;
    }
    .rating-badge {
        background-color: #388e3c;
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: bold;
    }
    .location-text {
        color: #616161;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar Filters ---
st.sidebar.header("🔍 Search Filters")
price_range = st.sidebar.slider("Price per night (₹)", 500, 10000, (1000, 5000))
prop_filter = st.sidebar.multiselect("Property Type", ["Townhouse", "Flagship", "Home", "Silver Key"], default=["Townhouse"])

# --- Main Content ---
st.title("Found 2 Properties in Gurgaon")

# Mock Data for Display
properties = [
    {
        "id": 1,
        "name": "Super OYO Townhouse 124 Sector 45",
        "location": "Sector 45, Near Huda City Centre, Gurgaon",
        "price": 1499,
        "old_price": 3200,
        "rating": 4.3,
        "lat": 28.4595,
        "lon": 77.0266,
        "img": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400"
    },
    {
        "id": 2,
        "name": "OYO Flagship 83445 Premium",
        "location": "DLF Phase 3, Cyber City, Gurgaon",
        "price": 999,
        "old_price": 2500,
        "rating": 4.1,
        "lat": 28.4900,
        "lon": 77.0800,
        "img": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=400"
    }
]

# Layout: 2/3 for listings, 1/3 for map
left_col, right_col = st.columns([1.5, 1])

with left_col:
    for prop in properties:
        # Check if property matches filters (Simplified logic)
        if price_range[0] <= prop["price"] <= price_range[1]:
            with st.container():
                # Using columns inside the container to mimic the 'card' look
                img_col, info_col = st.columns([1, 2])
                
                with img_col:
                    st.image(prop["img"], use_container_width=True)
                
                with info_col:
                    st.markdown(f"### {prop['name']}")
                    st.markdown(f"<p class='location-text'>📍 {prop['location']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<span class='rating-badge'>{prop['rating']} ★</span>", unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div style="margin: 15px 0;">
                            <span class="price-tag">₹{prop['price']}</span>
                            <span style="text-decoration: line-through; color: #9e9e9e; margin-left: 10px;">₹{prop['old_price']}</span>
                            <span style="color: #ff9800; font-weight: bold; margin-left: 10px;">{int((1 - prop['price']/prop['old_price'])*100)}% OFF</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"View Details & Book", key=f"btn_{prop['id']}"):
                        st.balloons()
                        st.info(f"Opening booking page for {prop['name']}...")
                
                st.divider()

with right_col:
    st.subheader("Map View")
    # Convert list to DataFrame for st.map
    df = pd.DataFrame(properties)
    st.map(df[['lat', 'lon']])
