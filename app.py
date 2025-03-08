import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests
import matplotlib.pyplot as plt



# Load the trained model
with open("crop_prediction_model.pkl", "rb") as file:
    model, le, scaler = pickle.load(file)

# Crop information dictionary
crop_info = {
    "Wheat": {"Best Season": "Winter", "Required Nutrients": "High Nitrogen", "Expected Yield": "3-4 tons/ha"},
    "Rice": {"Best Season": "Monsoon", "Required Nutrients": "High Phosphorus", "Expected Yield": "4-6 tons/ha"},
    "Maize": {"Best Season": "Summer", "Required Nutrients": "Balanced NPK", "Expected Yield": "5-7 tons/ha"},
    "Sugarcane": {"Best Season": "Tropical", "Required Nutrients": "High Potassium", "Expected Yield": "80-100 tons/ha"},
    "Barley": {"Best Season": "Winter", "Required Nutrients": "Moderate Nitrogen", "Expected Yield": "2-3 tons/ha"},
    "Soybean": {"Best Season": "Monsoon", "Required Nutrients": "High Phosphorus", "Expected Yield": "2-4 tons/ha"}
}

# Streamlit UI Setup
st.set_page_config(page_title="Smart Farming Assistant", layout="wide")

# Initialize session state for page tracking
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Sidebar for Navigation
with st.sidebar:
    st.title("🌾 Smart Farming Assistant")
    selection = st.radio("Go to", ["Home", "Crop Recommendation", "Demand Analysis", "Crop Monitoring",'agribot','chatbot'])
    st.session_state.page = selection

# Home Page
if st.session_state.page == "Home":
    st.title("🌱 Smart Farming Assistant")
    st.markdown("### Welcome to the Smart Farming Assistant! 🌾")
    st.write("Use this tool to get crop recommendations, analyze market demand, and monitor crop health.")

# Crop Recommendation Page
elif st.session_state.page == "Crop Recommendation":
    st.title("🌾 Crop Recommendation System")
    st.write("Provide the following details to get the best crop recommendation.")
    
    with st.form("crop_input_form"):
        st.subheader("🧪 Soil Composition")
        col1, col2, col3 = st.columns(3)
        with col1:
            N = st.number_input("Nitrogen (N)", min_value=0, max_value=150, value=50)
        with col2:
            P = st.number_input("Phosphorus (P)", min_value=0, max_value=150, value=30)
        with col3:
            K = st.number_input("Potassium (K)", min_value=0, max_value=150, value=40)

        st.subheader("🌡️ Environmental Factors")
        col4, col5 = st.columns(2)
        with col4:
            temperature = st.slider("Temperature (°C)", min_value=0, max_value=50, value=25)
            humidity = st.slider("Humidity (%)", min_value=0, max_value=100, value=70)
        with col5:
            ph = st.slider("Soil pH", min_value=0.0, max_value=14.0, value=6.5)
            rainfall = st.slider("Rainfall (mm)", min_value=0, max_value=500, value=200)

        st.subheader("🌱 Soil & Sunlight")
        with st.expander("More Soil & Sunlight Options"):
            soil_moisture = st.slider("Soil Moisture (%)", min_value=0, max_value=100, value=50)
            soil_type = st.selectbox("Soil Type", ["Sandy", "Clay", "Loamy", "Peaty", "Silty", "Chalky"])
            sunlight_exposure = st.slider("Sunlight Exposure (hours/day)", min_value=0, max_value=12, value=6)

        submit = st.form_submit_button("🌾 Predict Crop")

    if "crop_prediction" not in st.session_state:
        st.session_state.crop_prediction = None

    if submit:
        try:
            with st.spinner("Predicting the best crops..."):
                soil_type_encoded = ["Sandy", "Clay", "Loamy", "Peaty", "Silty", "Chalky"].index(soil_type)
                input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall, soil_moisture, soil_type_encoded, sunlight_exposure]])
                input_data = scaler.transform(input_data)

                # Get top 3 crop predictions
                probabilities = model.predict_proba(input_data)[0]
                top_3_indices = np.argpartition(probabilities, -3)[-3:]
                top_3_indices = top_3_indices[np.argsort(probabilities[top_3_indices])[::-1]]
                top_3_crops = le.inverse_transform(top_3_indices)

                st.subheader("🌾 Top 3 Recommended Crops")
                for i, crop in enumerate(top_3_crops, 1):
                    st.write(f"{i}. **{crop}**")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    # Display the prediction results
    if st.session_state.crop_prediction:
        top_3_crops, top_3_probs = st.session_state.crop_prediction
        st.subheader("🌾 Top 3 Recommended Crops")
        for i, (crop, prob) in enumerate(zip(top_3_crops, top_3_probs), 1):
            st.write(f"{i}. **{crop}** ({prob:.2%})")
            st.info(f"🌱 **Best Season:** {crop_info[crop]['Best Season']}")
            st.info(f"💊 **Required Nutrients:** {crop_info[crop]['Required Nutrients']}")
            st.info(f"🌾 **Expected Yield:** {crop_info[crop]['Expected Yield']}")

# Demand Analysis Page
# Demand Analysis Page
elif st.session_state.page == "Demand Analysis":
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
    
    #st.subheader("💰 Profitability Calculator")
    market_price = st.number_input("Market Price per ton ($)", min_value=100, max_value=1000, value=500)
    expected_yield = float(crop_info[selected_crop]["Expected Yield"].split('-')[0])  # Get min yield
    land_area = st.number_input("Land Area (hectares)", min_value=1, max_value=100, value=5)
    estimated_earning = market_price * expected_yield * land_area
    st.success(f"💵 **Estimated Earnings:** ${estimated_earning:.2f}") 
    




elif st.session_state.page == "Crop Monitoring":
    st.title("📡 Crop Monitoring System")
    st.write("This section will provide real-time monitoring of crop health and growth.")

    # Placeholder for real-time monitoring
    st.warning("🚀 Feature Coming Soon: AI-based crop health analysis and satellite data integration.")


