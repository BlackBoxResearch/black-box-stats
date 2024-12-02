import streamlit as st
import altair as alt
from static.elements import tile, metric_tile, gradient_text, animated_container
import random
from vega_datasets import data
import pandas as pd
import datetime as dt

now = dt.datetime.now(dt.timezone.utc)  # Get current time in UTC
current_time = now.hour + now.minute / 60  # Convert to hour with decimal minutes

def DashboardPage():
    with st.container(border=False):
        first_name = st.session_state.get("first_name", "User")
        
        st.subheader(f"Welcome back, {first_name}!", anchor=False)

        with tile("quote_tile", 25, border=True):
            # List of finance-related funny quotes
            quotes = [
                "*\"Inflation is necessary for my financial goals.\"* - **Fed Chair Powell**",
                "*\"Diversification is admitting you have no idea what's going to happen.\"* - **Every Wealth Manager Ever**",
                "*\"Remember, you can’t lose money if you don’t check your account.\"* - **Ancient Investing Proverb**",
                "*\"Bulls make money, bears make money, and my broker takes it all.\"* - **Every Trader**",
                "*\"Crypto is the future, just like flying cars were in the 80s.\"* - **Blockchain Evangelist**",
                "*\"If your portfolio doesn’t scare you a little, are you even trying?\"* - **Risk-Tolerant Optimist**",
                "*\"The market can stay irrational longer than you can stay solvent.\"* - **Trader in Tears**",
                "*\"HODL is just a fancy way of saying 'I forgot my password.'\"* - **Casual Crypto Investor**",
                "*\"Stop-losses are for quitters.\"* - **Overconfident Trader**",
                "*\"Retirement is a myth created by people who bought Apple in 1980.\"* - **Jealous Millennial**"
            ]

            # Select a random quote
            random_quote = random.choice(quotes)

            # Display the quote
            st.caption(random_quote)


#c8c8c8

        col1, col2, col3, col4 = st.columns(4, vertical_alignment="bottom")

        with col1:
            animated_container(
                key="Test", 
                content=f"""
                    <div style="line-height: 1.45;">
                        <p style="margin: 0; font-size: 0.75em; color: #E8E8E8;">Plan</p>
                        <p style="margin: 0; font-size: 1em; font-weight: bold; color: #E8E8E8;">Free</p>
                    </div>
                    """
                
                )

            # metric_tile(
            #     key="dashboard_plan_card", 
            #     stat="Plan", 
            #     value="Free", 
            #     height=40,
            #     type="secondary",
            #     border=False,
            #     tooltip=None
            #     )

        with col2:
            metric_tile(
                key="dashboard_stat_1", 
                stat="Stat 1", 
                value="Value", 
                height=40, 
                type="primary",
                border=True,
                tooltip=None
                )

        with col3:
            metric_tile(
                key="dashboard_stat_2", 
                stat="Stat 2", 
                value="Value", 
                height=40, 
                type="primary",
                border=True,
                tooltip=None
                )

        with col4:
            metric_tile(
                key="dashboard_stat_3", 
                stat="Stat 3", 
                value="Value", 
                height=40, 
                type="primary",
                border=True,
                tooltip=None
                )
        
        st.divider()

        animated_container(
            key="Test",
            content=f"""
                <div style="line-height: 1.8;">
                    <p style="margin: 0; font-size: 1em; color: #E8E8E8; ">Free</p>
                </div>
                """
            )
        
        with st.container(border=True):
            st.markdown("Plan")

if __name__ == "__main__":
    DashboardPage()
