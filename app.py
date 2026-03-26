import streamlit as st

# Page Config
st.set_page_config(page_title="OYO Clone - Search", layout="wide")

# Custom CSS to mimic OYO's clean look
st.markdown("""
    <style>
    .property-card {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        display: flex;
        background-color: white;
    }
    .price-tag {
        color: #d32f2f;
        font-size: 24px;
        font-weight: bold;
    }
    .rating-badge {
        background-color: #388e3c;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_dict=True)

# --- Sidebar Filters ---
st.sidebar.header("Filters")
price_range = st.sidebar.slider("Price Range", 500, 10000, (1000, 5000))
property_type = st.sidebar.multiselect("Property Type", ["Townhouse", "Silver Key", "Home", "Spot On"])
amenities = st.sidebar.checkbox("Free WiFi")

# --- Main Search Results ---
st.title("Properties in Gurgaon")

# Mock Data
properties = [
    {
        "name": "Super OYO Townhouse 124",
        "location": "Sector 45, Gurgaon",
        "price": 1499,
        "old_price": 3200,
        "rating": 4.3,
        "img": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400"
    },
    {
        "name": "OYO Flagship 83445",
        "location": "DLF Phase 3, Gurgaon",
        "price": 999,
        "old_price": 2500,
        "rating": 4.1,
        "img": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=400"
    }
]

col1, col2 = st.columns([2, 1])

with col1:
    for prop in properties:
        # Create a card-like layout using Streamlit columns
        with st.container():
            c1, c2 = st.columns([1, 2])
            with c1:
                st.image(prop["img"], use_container_width=True)
            with c2:
                st.subheader(prop["name"])
                st.write(f"📍 {prop['location']}")
                st.markdown(f"<span class='rating-badge'>{prop['rating']} ★</span>", unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div style="margin-top:10px;">
                        <span class="price-tag">₹{prop['price']}</span>
                        <span style="text-decoration: line-through; color: gray; margin-left: 10px;">₹{prop['old_price']}</span>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"View Details", key=prop['name']):
                    st.success("Redirecting to booking...")
            st.divider()

with col2:
    st.info("Map View (Integration)")
    # Streamlit has built-in map support
    map_data = {"lat": [28.4595], "lon": [77.0266]}
    st.map(map_data)
