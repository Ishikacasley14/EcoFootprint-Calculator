import streamlit as st
from PIL import Image
import base64
from io import BytesIO

# Define emission factors (example values, replace with accurate data)
EMISSION_FACTORS = {
    "India": {
        "Transportation": 0.14,  # kgCO2/km
        "Electricity": 0.82,  # kgCO2/kWh
        "Diet": 1.25,  # kgCO2/meal
        "Waste": 0.1  # kgCO2/kg
    },
    "United States": {
        "Transportation": 0.24,  # kgCO2/km
        "Electricity": 0.43,  # kgCO2/kWh
        "Diet": 1.6,  # kgCO2/meal
        "Waste": 0.29  # kgCO2/kg
    },
    "Germany": {
        "Transportation": 0.16,  # kgCO2/km
        "Electricity": 0.29,  # kgCO2/kWh
        "Diet": 1.2,  # kgCO2/meal
        "Waste": 0.1  # kgCO2/kg
    },
    "Brazil": {
        "Transportation": 0.12,  # kgCO2/km
        "Electricity": 0.16,  # kgCO2/kWh
        "Diet": 1.1,  # kgCO2/meal
        "Waste": 0.08  # kgCO2/kg
    }
}

# CO2 emissions data for each country
COUNTRY_CO2_DATA = {
    "India": "In 2023, CO2 emissions per capita for India was approximately 2.0 tons of CO2 per capita. This reflects a slight increase from 2021, influenced by ongoing economic growth and industrial activities.",
    "United States": "In 2023, CO2 emissions per capita for the United States was around 14.5 tons of CO2 per capita. This represents a continued decrease from earlier years due to various climate policies and increased adoption of renewable energy.",
    "Germany": "In 2023, CO2 emissions per capita for Germany was about 6.9 tons of CO2 per capita. Germany's emissions have continued to decrease, thanks to aggressive climate policies and a significant transition to renewable energy sources.",
    "Brazil": "In 2023, CO2 emissions per capita for Brazil was roughly 2.3 tons of CO2 per capita. The increase from 2021 is attributed to economic development and industrialization."
}

# Set wide layout and page name
st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")


##st.title("Personal Carbon Calculator App 🌲 ")

# Function to convert an image file to base64
def get_image_as_base64(image_path):
    img = Image.open(image_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Load and encode the image
image_path = "footprint.png"
image_base64 = get_image_as_base64(image_path)

# Create HTML content with inline image
html_content = f"""
<h1 style='display: inline;'>Personal Carbon Calculator App</h1>
<img src="data:image/png;base64,{image_base64}" width="50" style='vertical-align: middle; margin-left: 10px;'>
"""

# Display the title and image inline
st.markdown(html_content, unsafe_allow_html=True)

# Display the subheader and selectbox
st.subheader("🌍 Your Country")
country = st.selectbox("Select", list(EMISSION_FACTORS.keys()))

# Get emission factors for the selected country
factors = EMISSION_FACTORS[country]

# Create columns for input sliders and number input
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚗 Daily commute distance (in km)")
    distance = st.slider("Distance", 0.0, 100.0, key="distance_input")

    st.subheader("💡 Monthly electricity consumption (in kWh)")
    electricity = st.slider("Electricity", 0.0, 1000.0, key="electricity_input")

with col2:
    st.subheader("🍽️ Waste generated per week (in kg)")
    waste = st.slider("Waste", 0.0, 100.0, key="waste_input")

    st.subheader("🍽️ Number of meals per day")
    meals = st.number_input("Meals", 0, key="meals_input")

# Normalize inputs
if distance > 0:
    distance = distance * 365  # Convert daily distance to yearly
if electricity > 0:
    electricity = electricity * 12  # Convert monthly electricity to yearly
if meals > 0:
    meals = meals * 365  # Convert daily meals to yearly
if waste > 0:
    waste = waste * 52  # Convert weekly waste to yearly

# Calculate carbon emissions
transportation_emissions = factors["Transportation"] * distance
electricity_emissions = factors["Electricity"] * electricity
diet_emissions = factors["Diet"] * meals
waste_emissions = factors["Waste"] * waste

# Convert emissions to tonnes and round off to 2 decimal points
transportation_emissions = round(transportation_emissions / 1000, 2)
electricity_emissions = round(electricity_emissions / 1000, 2)
diet_emissions = round(diet_emissions / 1000, 2)
waste_emissions = round(waste_emissions / 1000, 2)

# Calculate total emissions
total_emissions = round(
    transportation_emissions + electricity_emissions + diet_emissions + waste_emissions, 2
)

if st.button("Calculate CO2 Emissions"):

    # Display results
    st.header("Results")

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Carbon Emissions by Category")
        st.info(f"🚗 Transportation: {transportation_emissions} tonnes CO2 per year")
        st.info(f"💡 Electricity: {electricity_emissions} tonnes CO2 per year")
        st.info(f"🍽️ Diet: {diet_emissions} tonnes CO2 per year")
        st.info(f"🗑️ Waste: {waste_emissions} tonnes CO2 per year")

    with col4:
        st.subheader("Total Carbon Footprint")
        st.success(f"🌍 Your total carbon footprint is: {total_emissions} tonnes CO2 per year")
        st.warning(COUNTRY_CO2_DATA[country]) 