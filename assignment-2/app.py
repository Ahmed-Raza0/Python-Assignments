import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Securely fetch GEMINI API Key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Function to get AI explanation from Gemini
def get_ai_explanation(conversion_type, input_value, result):
    prompt = f"Explain how {input_value} {conversion_type} is converted to {result} in a simple way."

    try:
        # Generate explanation using the Gemini client
        response = client.models.generate_content(
            model="gemini-2.0-flash",  # Ensure this model is correct
            contents=prompt
        )
        explanation = response.text.strip()
        if not explanation:
            explanation = "The explanation was not returned by the AI model. Please check the API configuration."
        return explanation
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("Unit Converter with AI Explanations")

# Styling for the UI
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #1e3c72, #2a5298); /* Gradient background */
        color: white;
        font-family: 'Arial', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #1e3c72, #2a5298); /* Semi-transparent background */
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px); /* Blur effect for glassmorphism */
    }
    h1 {
        text-align: center;
        font-size: 48px;
        color: #ff9f43; /* Vibrant orange */
        font-weight: bold;
        margin-bottom: 20px;
    }
    .stButton>button {
        background: #ff9f43; /* Vibrant orange */
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 18px;
        box-shadow: 0px 4px 12px rgba(255, 159, 67, 0.4);
        transition: 0.3s;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: #ff6f61; /* Coral pink on hover */
        transform: scale(1.05);
    }
    .result-box {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        background: rgba(255, 255, 255, 0.2);
        padding: 25px;
        border-radius: 15px;
        margin-top: 20px;
        margin-bottom: 15px;
        box-shadow: 0px 4px 12px rgba(255, 159, 67, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .result-box p {
        margin-bottom: 0;
        font-size: 22px;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        font-size: 16px;
        color: white;
        opacity: 0.7;
    }
    .footer a {
        color: #ff9f43; /* Vibrant orange */
        text-decoration: none;
    }
    .footer a:hover {
        color: #ff6f61; /* Coral pink on hover */
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown("<h1>Unit Converter</h1>", unsafe_allow_html=True)
st.write("Easily convert between units of measurement with a modern design.")

# Sidebar menu for conversion type
conversion_type = st.sidebar.selectbox("Choose Conversion Type to Convert", ["Length", "Weight", "Temperature"])
value = st.number_input("Enter Value", min_value=0.0, format="%.2f")

col1, col2 = st.columns(2)

# Conversion logic
result = None  # Initialize result as None
if conversion_type == "Length":
    with col1:
        from_unit = st.selectbox("From", ["Meters", "Kilometers", "Millimeters", "Miles", "Yards", "Centimeters", "Feet", "Inches"])
    with col2:
        to_unit = st.selectbox("To", ["Meters", "Kilometers", "Millimeters", "Miles", "Yards", "Centimeters", "Feet", "Inches"])
        
    conversion_factors = {
        "Meters-Kilometers": 0.001, "Kilometers-Meters": 1000,
        "Meters-Millimeters": 1000, "Millimeters-Meters": 0.001,
        "Meters-Miles": 0.000621371, "Miles-Meters": 1609.34,
        "Meters-Yards": 1.09361, "Yards-Meters": 0.9144,
        "Meters-Centimeters": 100, "Centimeters-Meters": 0.01,
        "Meters-Feet": 3.28084, "Feet-Meters": 0.3048,
        "Meters-Inches": 39.3701, "Inches-Meters": 0.0254,
        "Inches-Feet": 1 / 12, "Feet-Inches": 12
    }
    key = f"{from_unit}-{to_unit}"
    result = value * conversion_factors.get(key, 1)

elif conversion_type == "Weight":
    with col1:
        from_unit = st.selectbox("From", ["Kilograms", "Grams", "Milligrams", "Pounds", "Ounces"])
    with col2:
        to_unit = st.selectbox("To", ["Kilograms", "Grams", "Milligrams", "Pounds", "Ounces"])
        
    conversion_factors = {
        "Kilograms-Grams": 1000, "Grams-Kilograms": 0.001,
        "Kilograms-Milligrams": 1000000, "Milligrams-Kilograms": 0.000001,
        "Kilograms-Pounds": 2.20462, "Pounds-Kilograms": 0.453592,
        "Kilograms-Ounces": 35.274, "Ounces-Kilograms": 0.0283495
    }
    key = f"{from_unit}-{to_unit}"
    result = value * conversion_factors.get(key, 1)

elif conversion_type == "Temperature":
    with col1:
        from_unit = st.selectbox("From", ["Celsius", "Fahrenheit", "Kelvin"])
    with col2:
        to_unit = st.selectbox("To", ["Celsius", "Fahrenheit", "Kelvin"])
        
    if from_unit == "Celsius" and to_unit == "Fahrenheit":
        result = (value * 1.8) + 32
    elif from_unit == "Fahrenheit" and to_unit == "Celsius":
        result = (value - 32) / 1.8
    elif from_unit == "Celsius" and to_unit == "Kelvin":
        result = value + 273.15
    elif from_unit == "Kelvin" and to_unit == "Celsius":
        result = value - 273.15
    elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
        result = (value - 32) / 1.8 + 273.15
    elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
        result = (value - 273.15) * 1.8 + 32
    else:
        result = value

# Display result and AI explanation only if result is valid
if result is not None:
    st.markdown(f"<div class='result-box'>{value} {from_unit} is equal to {result:.2f} {to_unit}</div>", unsafe_allow_html=True)
    # AI Explanation for conversion
    explanation = get_ai_explanation(conversion_type, value, result)
    st.info(f"AI Explanation: {explanation}")
else:
    st.warning("Please enter a valid input and ensure the conversion type is selected.")

# Footer
st.markdown("<div class='footer'>Developed with ❤️ by <a href='https://github.com/Ahmed-Raza0' target='_blank' style='color: #ff9f43; text-decoration: none;'>Ahmed Raza</a> using Streamlit</div>", unsafe_allow_html=True)
