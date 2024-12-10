import streamlit as st

def LeaderboardPage():
    with st.container(border=False):
        st.subheader("Leaderboard", anchor=False)
        st.markdown("**Welcome to the Black Box Stats Leaderboards!**")
        st.caption("Compare your trading performance with the community, compete on leaderboards, and win prizes by showcasing your accounts and systems.")
        
        leaderboard_help_string='''
        **Leaderboards**
        \n\n🌟 **Showcase Your Best:** Select which connected accounts or systems to make public in your settings.
        \n\n📊 **Black Box Score:** Your score reflects profitability, consistency, and risk-adjusted returns—higher scores mean stronger, more stable trading.
        \n\n🏆 **Compete for Rewards:** Top-ranked traders earn recognition, free Premium credits, or community prizes weekly and monthly.
        \n\n🔒 **Privacy Options:** Prefer to stay private? Keep accounts and systems set to “Private” in your settings.
        \n\n**Ready to climb the ranks?** Update your visibility settings and join the competition!
        '''

        st.markdown("**How It Works:**", help=leaderboard_help_string)

        accounts_tab, systems_tab = st.tabs(['Accounts Leaderboard', 'Systems Leaderboard'])

        with accounts_tab:
            st.subheader("Accounts Leaderboard", anchor=False)
            st.caption('''
            This tab showcases public trading accounts, ranked by their Black Box Score—a measure of profitability, risk management, and consistency.
            ''')

        with systems_tab:
            st.subheader("Systems Leaderboard", anchor=False)
            st.caption('''
            This tab ranks user-created systems—portfolios combining multiple accounts—by their aggregated performance and Black Box Score, highlighting your ability to build balanced, diversified strategies.
            ''')

if __name__ == "__main__":
    LeaderboardPage()
