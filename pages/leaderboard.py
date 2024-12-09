import streamlit as st

def LeaderboardPage():
    with st.container(border=False):
        st.subheader("Leaderboard", anchor=False)
        st.markdown("**Welcome to the Black Box Stats Leaderboards!**")
        st.caption("Here, you can see how your trading performance stacks up against other members of the community. By making your accounts and systems publicly visible, you can earn a spot on our leaderboards and compete for weekly or monthly prizes.")
        
        leaderboard_help_string='''
        **Leaderboards**
        \n\nChoose which of your connected accounts or custom-built systems you’d like to make public.
        \n\nEach eligible account and system is assigned a proprietary Black Box Score, reflecting factors like profitability, consistency, and risk-adjusted returns. Higher scores indicate more stable, skillful trading performance.
        \n\nThe top-ranked accounts and systems on our leaderboards at the end of each week and month may earn recognition, free Premium subscription credits, or other community prizes.
        \n\n**Ready to participate?** Head to your Accounts/Systems settings to toggle visibility and start climbing the ranks, or if you prefer to remain private, simply keep your accounts or systems set to “Private” in your settings.'''

        st.markdown("**How It Works:**", help=leaderboard_help_string)

        accounts_tab, systems_tab = st.tabs(['Accounts Leaderboard', 'Systems Leaderboard'])

        with accounts_tab:
            st.subheader("Accounts Leaderboard", anchor=False)
            st.caption('''
            This tab showcases individual trading accounts from our users who’ve chosen to make their performance public. Each account’s Black Box Score, return rates, drawdown metrics, and consistency indicators are used to rank them against one another.
            ''')

        with systems_tab:
            st.subheader("Systems Leaderboard", anchor=False)
            st.caption('''
            This tab ranks user-created systems — portfolios composed of one or more accounts—based on their aggregated performance and Black Box Score. Systems let you demonstrate your skill in constructing balanced, diversified strategies, not just picking single accounts.
        ''')

if __name__ == "__main__":
    LeaderboardPage()
