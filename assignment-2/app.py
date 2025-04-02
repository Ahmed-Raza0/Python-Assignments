import streamlit as st
import re


def password_strength(password):
    score = 0


    
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1

    
    if re.search(r'[a-z]', password):
        score += 1
    if re.search(r'[A-Z]', password):
        score += 1
    if re.search(r'[0-9]', password):
        score += 1
    if re.search(r'[\W_]', password):   
        score += 1

    
    if score <= 2:
        strength = "Very Weak"
    elif score == 3:
        strength = "Weak"
    elif score == 4:
        strength = "Moderate"
    elif score == 5:
        strength = "Strong"
    else:
        strength = "Very Strong"
    
    return strength, score

 
def custom_css():
    st.markdown("""
        <style>
            body {
                background-color: #f4f7fa;
                font-family: 'Arial', sans-serif;
            }
            .main {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            .header {
                text-align: center;
                color: #4CAF50;
                font-size: 2em;
            }
            .input-container {
                margin-top: 20px;
                margin-bottom: 20px;
            }
            .submit-btn {
                background-color: #4CAF50;
                color: white;
                padding: 12px 20px;
                border: none;
                border-radius: 5px;
                font-size: 1em;
                cursor: pointer;
                width: 100%;
                transition: background-color 0.3s ease;
            }
            .submit-btn:hover {
                background-color: #45a049;
            }
            .tips {
                font-size: 0.9em;
                margin-top: 20px;
                padding: 15px;
                border-radius: 8px;
            }
            .warning-text {
                color: #f44336;
            }
            .success-text {
                color: #4CAF50;
            }
        </style>
    """, unsafe_allow_html=True)


def main():
    custom_css()
    
    st.markdown('<div class="main">', unsafe_allow_html=True)
    
    st.markdown('<div class="header">🔐Password Strength Meter</div>', unsafe_allow_html=True)

    password = st.text_input("🗝️Enter your password:", type="password")
    submit_button = st.button("Submit", key="submit")

    if submit_button and password:
        
        strength, score = password_strength(password)
 
            
            
        st.write(f"Password Strength: {strength}")
            
        if strength == "Very Weak":
                st.warning("Your password is too weak! Try using a combination of upper and lower case letters, numbers, and special characters.")
        elif strength == "Weak":
                st.warning("Consider making your password longer and including a variety of characters.")
        elif strength == "Moderate":
                st.success("Your password is decent, but could be stronger with more complexity.")
        elif strength == "Strong":
                st.success("Your password is strong, but you could still add more variety!")
        else:
                st.success("Great job! Your password is very strong.")
            
            
            

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="tips">', unsafe_allow_html=True)
    st.write("### Tips for creating a stronger password:")
    st.write("✅ Use at least 12 characters.")
    st.write("✅ Combine uppercase and lowercase letters.")
    st.write("✅ Add numbers and special characters (e.g., !@#$%).")
    st.write("✅ Avoid common words or phrases.")
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
