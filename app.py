import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests
import matplotlib.pyplot as plt

# Streamlit UI Setup
st.set_page_config(page_title="Smart Farming Assistant", layout="wide")

# Initialize session state for page tracking
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Sidebar for Navigation
with st.sidebar:
    st.title("🌾 Smart Farming Assistant")
    selection = st.radio("Go to", ["Home", "Crop Recommendation", "Demand Analysis", "Crop Monitoring","agribot"])
    st.session_state.page = selection

# Home Page
if st.session_state.page == "Home":
    st.title("🌱 Smart Farming Assistant")
    st.markdown("### Welcome to the Smart Farming Assistant! 🌾")
    st.write("Use this tool to get crop recommendations, analyze market demand, and monitor crop health.")

# Load selected page
elif selection == "Crop Recommendation":
    import recommendation
elif selection == "Demand Analysis":
    import demand
elif selection == "Crop Monitoring":
    import monitoring
elif selection == "agribot":
    import agribot