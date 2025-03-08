import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt

crop_info = {
    "Wheat": {"Best Season": "Winter", "Required Nutrients": "High Nitrogen", "Expected Yield": "3-4 tons/ha"},
    "Rice": {"Best Season": "Monsoon", "Required Nutrients": "High Phosphorus", "Expected Yield": "4-6 tons/ha"},
    "Maize": {"Best Season": "Summer", "Required Nutrients": "Balanced NPK", "Expected Yield": "5-7 tons/ha"},
    "Sugarcane": {"Best Season": "Tropical", "Required Nutrients": "High Potassium", "Expected Yield": "80-100 tons/ha"},
    "Barley": {"Best Season": "Winter", "Required Nutrients": "Moderate Nitrogen", "Expected Yield": "2-3 tons/ha"},
    "Soybean": {"Best Season": "Monsoon", "Required Nutrients": "High Phosphorus", "Expected Yield": "2-4 tons/ha"}
}

st.title("📊 Crop Demand Analysis")
st.write("Analyze the demand for different crops before planting.")

    # Select a crop
crop_options = list(crop_info.keys())
selected_crop = st.selectbox("🔍 Select a Crop to Analyze", crop_options)

    # Display crop-specific details
st.subheader(f"📈 Demand Insights for {selected_crop}")
st.info(f"🌱 **Best Season:** {crop_info[selected_crop]['Best Season']}")
st.info(f"💊 **Required Nutrients:** {crop_info[selected_crop]['Required Nutrients']}")
st.info(f"🌾 **Expected Yield:** {crop_info[selected_crop]['Expected Yield']}")

    # Live Market Price Integration (API Placeholder)
st.subheader("💰 Live Market Price")
api_url = f"https://api.example.com/prices?crop={selected_crop}"  # Replace with actual API
try:
        response = requests.get(api_url)
        market_price = response.json().get("price", "Data Unavailable")
except:
        market_price = "Data Unavailable"
st.success(f"**Current Market Price for {selected_crop}:** ${market_price} per ton")

    # Simulated demand trend data
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
demand_values = np.random.randint(50, 200, size=12)

    # Supply & Demand Trends Visualization
st.subheader("📊 Supply & Demand Trends")
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(months, demand_values, marker='o', linestyle='-', color='blue', linewidth=2, label="Market Demand")
ax.fill_between(months, demand_values, color='blue', alpha=0.2)
ax.set_xlabel("Months")
ax.set_ylabel("Market Demand")
ax.set_title(f"Supply & Demand Trends for {selected_crop}")
ax.legend()
st.pyplot(fig)

    # Region-wise Demand Analysis
st.subheader("📍 Region-wise Demand Analysis")
user_location = st.text_input("Enter your location:", "Your City")
region_demand = np.random.choice(["High", "Medium", "Low"])
st.warning(f"📌 Demand for **{selected_crop}** in {user_location}: **{region_demand}**")

    # Profitability Calculator
st.subheader("💰 Profitability Calculator")
market_price = st.number_input("Market Price per ton ($)", min_value=100, max_value=1000, value=500)
expected_yield = float(crop_info[selected_crop]["Expected Yield"].split('-')[0])  # Get min yield
land_area = st.number_input("Land Area (hectares)", min_value=1, max_value=100, value=5)
estimated_earning = market_price * expected_yield * land_area
st.success(f"💵 **Estimated Earnings:** ${estimated_earning:.2f}")