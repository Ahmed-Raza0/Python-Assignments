import streamlit as st

st.title("BMI Calculator")

height = st.number_input("Enter your height (cm):", min_value=50, max_value=300)
weight = st.number_input("Enter your weight (kg):", min_value=10, max_value=300)

if st.button("Calculate BMI"):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    st.write(f"Your BMI is **{bmi:.2f}**")

    if bmi < 18.5:
        st.warning("Underweight")
    elif 18.5 <= bmi < 24.9:
        st.success("Normal weight")
    elif 25 <= bmi < 29.9:
        st.info("Overweight")
    else:
        st.error("Obese")