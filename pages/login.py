from utils.auth import check_login, register_user
from static.elements import gradient_button

import streamlit as st

countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia",
    "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium",
    "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
    "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad",
    "Chile", "China", "Colombia", "Comoros", "Congo, Democratic Republic of the", "Congo, Republic of the",
    "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic",
    "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji",
    "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea",
    "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq",
    "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, North",
    "Korea, South", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya",
    "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta",
    "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia",
    "Montenegro", "Morocco", "Mozambique", "Myanmar (Burma)", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand",
    "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea",
    "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis",
    "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia",
    "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia",
    "South Africa", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan",
    "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan",
    "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan",
    "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]

def open_register_dialog():
    with st.form("register_form", border=False):
        col1, col2 = st.columns(2)
        first_name = col1.text_input("First name")
        last_name = col2.text_input("Last name")
        email = col1.text_input("Email")
        country = col2.selectbox("Country", countries)
        password = col1.text_input("Password", type="password")
        repeat_password = col2.text_input("Repeat password", type="password")
        password_hint = st.text_input("Password hint")
        marketing_preferences = st.checkbox("Opt out of communications")
        terms_and_conditions = st.checkbox("I agree to the Terms of Use")

        if st.form_submit_button("Register", use_container_width=True, type='primary'):
            if password != repeat_password:
                st.error("Passwords do not match.")
            elif not first_name or not last_name or not email or not password:
                st.error("All fields are required.")
            else:
                register_user(first_name, last_name, email, country, password, password_hint)

def LoginPage():
    with st.container(border=False):
        #st.image(image="static/bbs_type_logo.png")
        st.subheader("Sign up today for free!", anchor=False)
        st.caption("Or sign into your account")
    

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if gradient_button("Sign In", "sign_in_button", ":material/login:"):
            user_id, email, first_name, last_name, subscription_level = check_login(email, password)
            if email:
                # Reset the logged_out state when logging in successfully
                st.session_state["logged_out"] = False
                st.session_state["logged_in"] = True
                st.session_state["user_id"] = user_id
                st.session_state["first_name"] = first_name
                st.session_state["last_name"] = last_name
                st.session_state["email"] = email
                st.session_state["subscription_level"] = subscription_level

                st.success(f"Logged in successfully as {first_name}!")
                st.session_state["current_page"] = "Dashboard"

                st.rerun()
            else:
                st.error("Incorrect email or password. Please try again.")  

        # Register button to open the registration dialog
        if st.button("Register", use_container_width=True, type='secondary'):
            open_register_dialog()

if __name__ == "__main__":
    LoginPage()
