import streamlit as st
import numpy as np
import pandas as pd
import pickle

# Cache the model loading
@st.cache_resource
def load_model():
    with open("crop_prediction_model.pkl", "rb") as file:
        return pickle.load(file)

model, le, scaler = load_model()

# Crop information dictionary
crop_info = {
    "Wheat": {"Best Season": "Winter", "Required Nutrients": "High Nitrogen", "Expected Yield": "3-4 tons/ha"},
    "Rice": {"Best Season": "Monsoon", "Required Nutrients": "High Phosphorus", "Expected Yield": "4-6 tons/ha"},
    "Maize": {"Best Season": "Summer", "Required Nutrients": "Balanced NPK", "Expected Yield": "5-7 tons/ha"},
    "Sugarcane": {"Best Season": "Tropical", "Required Nutrients": "High Potassium", "Expected Yield": "80-100 tons/ha"},
    "Barley": {"Best Season": "Winter", "Required Nutrients": "Moderate Nitrogen", "Expected Yield": "2-3 tons/ha"},
    "Soybean": {"Best Season": "Monsoon", "Required Nutrients": "High Phosphorus", "Expected Yield": "2-4 tons/ha"}
}

st.title("🌾 Crop Recommendation System")
st.write("Provide the following details to get the best crop recommendation.")

# User Input Form
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
if "agribot_response" not in st.session_state:
    st.session_state.agribot_response = None

# Run prediction only when the button is clicked
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
            top_3_probs = probabilities[top_3_indices]

            # Store results in session state
            st.session_state.crop_prediction = (top_3_crops, top_3_probs)

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

    # AgriBot Integration
    st.subheader("🤖 AgriBot Response")
    st.write("Here is AgriBot's analysis based on your input:")
    st.session_state.agribot_response = "AgriBot response to user input"
    st.write(f"**AgriBot:** {st.session_state.agribot_response}")