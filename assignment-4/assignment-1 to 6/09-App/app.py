import streamlit as st

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "About", "Projects", "Contact"])

if page == "Home":
    st.title("Welcome to My Streamlit Website")
    st.write("This is a quick website built using Streamlit!")

elif page == "About":
    st.header("About Me")
    st.write("I'm Sidra Raza, a Python & Web Dev enthusiast 💻🌸")

elif page == "Projects":
    st.header("Projects")
    st.write("- BMI Calculator")
    st.write("- Portfolio Website")
    st.write("- Resume Builder")

elif page == "Contact":
    st.header("Contact Me")
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")
    if st.button("Send"):
        st.success("Message sent (not really, this is just a demo 😉)")