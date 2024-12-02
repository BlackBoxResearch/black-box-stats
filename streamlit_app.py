import streamlit as st
from static.elements import animated_container, promo_container
from streamlit_extras.bottom_container import bottom
from st_social_media_links import SocialMediaIcons
from pages import login, profile, dashboard, logout, systems, settings, support, accounts

primary_background = '#111111'
secondary_background = '#171717'
dark_text_color = '#171717'
light_text_color = '#E8E8E8'
color_1 = '#5A85F3'
color_2 = '#CDFFD8'

st.set_page_config(layout="centered")

# Define pages with icons
login_page = st.Page(page=login.LoginPage, title="Login", icon=":material/login:")
dashboard_page = st.Page(page=dashboard.DashboardPage, title="Dashboard", icon=":material/dashboard:")
systems_page = st.Page(page=systems.SystemsPage, title="Systems", icon=":material/stacked_line_chart:")
support_page = st.Page(page=support.SupportPage, title="Support", icon=":material/support_agent:")
profile_page = st.Page(page=profile.ProfilePage, title="My Profile", icon=":material/account_circle:")
settings_page = st.Page(page=settings.SettingsPage, title="Settings", icon=":material/settings:")
logout_page = st.Page(page=logout.LogoutPage, title="Logout", icon=":material/logout:")
accounts_page = st.Page(page=accounts.AccountsPage, title="My Accounts", icon=":material/group:")

# Group pages for logged-out users
logged_out_pages = [login_page]

# Group pages for logged-in users
logged_in_pages = {
    "Home": [dashboard_page, accounts_page, systems_page],
    "Settings": [profile_page, settings_page, logout_page]  # Logout page added here
}

def create_navigation(pages):
    # Create the navigation sidebar
    selected_page = st.navigation(pages, position="sidebar")
    # Run the selected page function
    selected_page.run()

def main():
    # Check if user is already logged in
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # Check if user has logged out and reset if necessary
    if "logged_out" not in st.session_state:
        st.session_state["logged_out"] = False

    # Display pages based on login state
    if st.session_state["logged_in"]:
        st.logo(image="static/bbs_type_logo.png", size="large")

        with st.sidebar:   
            promo_container(
                key="pro-lifetime_promo", 
                content=f'''
                    <div>
                        <h3 style="
                            font-size: 1.5em;
                            font-weight: bold;
                            text-align: left;
                            font-family: 'Segoe UI', sans-serif;
                            margin: 0;
                            color: {light_text_color};">
                            Upgrade to Pro for Life
                        </h3>
                        <p style="
                            font-size: 1em; 
                            font-weight: bold; 
                            font-family: 'Segoe UI', sans-serif;
                            background: linear-gradient(90deg, {color_1}, {color_2}); 
                            -webkit-background-clip: text; 
                            -webkit-text-fill-color: transparent;
                            margin: 5px 0;">
                            Limited lifetime deal ends soon!
                        </p>
                        <p style="
                            font-size: 0.85em; 
                            font-family: 'Segoe UI', sans-serif;
                            color: #CCCCCC; 
                            margin: 10px 0;">
                            After this exclusive early access deal, we are switching to monthly/annual pricing.
                        </p>
                        <div style="text-align: center; margin-top: 20px;">
                            <a href="https://pay.analytiq.trade/b/test_6oE0043QndEzbLi5kk" 
                                target="_blank" 
                                style="
                                    display: inline-block; 
                                    padding: 0.5em 1em; 
                                    background-image: linear-gradient(90deg, {color_1}, {color_2}); 
                                    color: {dark_text_color}; 
                                    text-decoration: none; 
                                    font-size: 0.85em;
                                    border-radius: 0.5rem;
                                    box-shadow: 20px 0 100px {color_1}40;
                                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                                "
                                >
                                ✨ Upgrade Now
                            </a>
                        </div>
                    </div>
                '''
                )

        create_navigation(logged_in_pages)
    else:
        create_navigation(logged_out_pages)

    with bottom():
        social_media_links = [
            "https://x.com/blackboxstats",
            "https://www.instagram.com/blackboxstats"
        ]

        social_media_icons = SocialMediaIcons(social_media_links, colors=["#ffffff", "#ffffff"])

        social_media_icons.render()

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
