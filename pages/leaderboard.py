import streamlit as st

def LeaderboardPage():
    with st.container(border=False):
        st.subheader("Leaderboard", anchor=False)
        st.caption( '''
                    **Welcome to the Black Box Stats Leaderboards!**

                    Here, you can see how your trading performance stacks up against other members of the community. By making your accounts and systems publicly visible, you can earn a spot on our leaderboards and compete for weekly or monthly prizes.
                    ''')
        
        leaderboard_help_string = '''Test String'''

'''

                    **1. Public Visibility:**

                    Choose which of your connected accounts or custom-built systems you’d like to make public. Public entries become eligible for our leaderboards and competitions.
                    
                    **2. Black Box Score:**

                    Each eligible account and system is assigned a proprietary Black Box Stats (BBS) Score, reflecting factors like profitability, consistency, and risk-adjusted returns.
                    
                    Higher BBS Scores indicate more stable, skillful trading performance.
                                    
                    **3. Compete for Prizes:**

                    The top-ranked accounts and systems on our leaderboards at the end of each week and month may earn recognition, free Premium subscription credits, or other community prizes.
                    
                    Participation is optional—if you prefer to remain private, simply keep your accounts or systems set to “Private” in your settings.
                    
                    **Ready to participate?**

                    Head to your My Profile or Accounts/Systems settings to toggle visibility and start climbing the ranks!
                   
                   '''


        st.markdown("**How It Works:**", help=leaderboard_help_string)

        accounts_tab, systems_tab = st.tabs(['Accounts Leaderboard', 'Systems Leaderboard'])

        with accounts_tab:
            st.subheader("Accounts Leaderboard", anchor=False)
            st.caption('''
                        This tab showcases individual trading accounts from our users who’ve chosen to make their performance public. Each account’s BBS Score, return rates, drawdown metrics, and consistency indicators are used to rank them against one another.

                        **Key Features:**

                        Ranking by BBS Score: Accounts are listed from highest to lowest BBS Score. Hover over or tap on a trader’s BBS Score to see a quick breakdown of what went into it.
                        
                        Performance Snapshots: Quickly review key metrics (e.g., monthly ROI, average win/loss ratio, maximum drawdown) to understand what sets top performers apart.
                        
                        Timeframe Filters: Adjust the leaderboard to show top performers over different periods (weekly, monthly) to spot consistent winners versus short-term standouts.
                        
                        **How to Get Listed Here:**

                        Set Your Account to Public: In your Accounts page settings, enable “Public Visibility” for any account you’d like to feature. Your trading data will be anonymized—only a display name, performance metrics, and BBS Score are shown.
                        
                        Meet Minimum Criteria: Some competitions may require a minimum number of trading days, a live (not demo) account, and adherence to community guidelines to qualify for prizes.

''')

        with systems_tab:
            st.subheader("Systems Leaderboard", anchor=False)
            st.caption('''
                        This tab ranks user-created “systems”—portfolios composed of one or more accounts—based on their aggregated performance and BBS Score. Systems let you demonstrate your skill in constructing balanced, diversified strategies, not just picking single accounts.

                        **Key Features:**

                        Aggregated BBS Score: Systems receive their own BBS Score, taking into account the combined returns, risk management, and consistency of all included accounts.
                        
                        Diversification & Strategy Insights: Performance metrics highlight how well-rounded a system is, helping you spot top-quartile portfolio constructors or specialized strategy curators.
                        
                        Comparison Tools: Some views let you compare two or more systems side-by-side, so you can see how top-tier systems differentiate themselves in terms of drawdowns, performance consistency, and asset allocation.
                        
                        **How to Get Listed Here:**

                        Make Your System Public: In the Systems page, select the system(s) you want to showcase and enable the “Public Visibility” setting.
                        
                        Meet Eligibility Criteria: As with accounts, systems often need to meet a minimum age or number of trades to appear on the leaderboard and be eligible for prizes. Systems composed entirely of demo accounts may not qualify for certain competitions.
''')

if __name__ == "__main__":
    LeaderboardPage()
