import streamlit as st
from static.elements import animated_container, promo_container
from streamlit_extras.bottom_container import bottom
from st_social_media_links import SocialMediaIcons
from pages import login, profile, dashboard, logout, systems, settings, support, accounts, leaderboard, pricing, changelog

primary_background = '#111111'
secondary_background = '#171717'
dark_text_color = '#171717'
light_text_color = '#E8E8E8'
color_1 = '#5A85F3'
color_2 = '#CDFFD8'

st.set_page_config(
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

with open('./static/styles.css') as f_css:
    css = f_css.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

with open('./static/styles.html') as f_html:
    html = f_html.read()

st.markdown(html, unsafe_allow_html=True)

# # # Custom CSS to hide the header
# st.markdown(
#     """
#     <style>
#         /* Hide the Streamlit header */
#         header {visibility: hidden;}
#     </style>
#     """,
#     unsafe_allow_html=True
# )


# Define pages with icons
login_page = st.Page(page=login.LoginPage, title="Login", icon=":material/login:")
dashboard_page = st.Page(page=dashboard.DashboardPage, title="Dashboard", icon=":material/dashboard:")
systems_page = st.Page(page=systems.SystemsPage, title="Systems", icon=":material/stacked_line_chart:")
support_page = st.Page(page=support.SupportPage, title="Support", icon=":material/support_agent:")
profile_page = st.Page(page=profile.ProfilePage, title="My Profile", icon=":material/account_circle:")
settings_page = st.Page(page=settings.SettingsPage, title="Settings", icon=":material/settings:")
logout_page = st.Page(page=logout.LogoutPage, title="Logout", icon=":material/logout:")
accounts_page = st.Page(page=accounts.AccountsPage, title="Accounts", icon=":material/group:")
leaderboard_page = st.Page(page=leaderboard.LeaderboardPage, title="Leaderboard", icon=":material/social_leaderboard:")
pricing_page = st.Page(page=pricing.PricingPage, title="Pricing", icon=":material/payments:")
changelog_page = st.Page(page=changelog.ChangelogPage, title="Change Log", icon=":material/construction:")

# Group pages for logged-out users
logged_out_pages = [login_page]

# Group pages for logged-in users
logged_in_pages = {
    "Home": [dashboard_page, accounts_page, systems_page, leaderboard_page, pricing_page],
    "Settings": [profile_page, changelog_page, settings_page, logout_page]  # Logout page added here
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
        st.logo(image="static/analytiq_type_logo.png", size="large", icon_image="static/analytiq_icon.png")

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
