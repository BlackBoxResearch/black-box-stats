import streamlit as st
import altair as alt
from static.elements import tile, metric_tile, gradient_text
import random
from vega_datasets import data
import pandas as pd
import datetime as dt

now = dt.datetime.now(dt.timezone.utc)  # Get current time in UTC
current_time = now.hour + now.minute / 60  # Convert to hour with decimal minutes

def DashboardPage():
    with st.container(border=False):
        first_name = st.session_state.get("first_name", "User")
        
        gradient_text(f"Welcome back, {first_name}!", "3em")

        with tile("quote_tile", 25):
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

        col1, col2, col3, col4 = st.columns(4, vertical_alignment="bottom")

        with col1:
            metric_tile(
                key="dashboard_plan_card", 
                stat="Plan", 
                value="Free", 
                height=55, 
                type="secondary", 
                tooltip=None
                )

        with col2:
            metric_tile(
                key="dashboard_stat_1", 
                stat="Stat 1", 
                value="Value", 
                height=55, 
                type="primary", 
                tooltip=None
                )

        with col3:
            metric_tile(
                key="dashboard_stat_2", 
                stat="Stat 2", 
                value="Value", 
                height=55, 
                type="primary", 
                tooltip=None
                )

        with col4:
            metric_tile(
                key="dashboard_stat_3", 
                stat="Stat 3", 
                value="Value", 
                height=55, 
                type="primary", 
                tooltip=None
                )

        st.divider()

        col1, col2 = st.columns([2.5,1], vertical_alignment="bottom")

        with col1:
            with tile("session_map", 460):
                st.markdown("**Trading Session**")

                # Source of land data
                source = alt.topo_feature(data.world_110m.url, 'countries')

                # Base map with adjusted projection to crop empty areas
                map_chart = alt.Chart(source).mark_geoshape(
                    fill='#adadad', stroke='#171717'
                ).transform_filter(
                    "datum.id != '010'"  # Exclude Antarctica
                ).project(
                    'naturalEarth1',  # Projection
                    scale=150,  # Adjust scale to zoom in and crop
                    translate=[300, 200]  # Center map horizontally and vertically
                )

                # Vertical line for current time (hour + minutes)
                time_line = alt.Chart(pd.DataFrame({'current_time': [current_time]})).mark_rule(
                    color='#94B9FF', strokeWidth=2
                ).encode(
                    x=alt.X('current_time:Q', title="Current Time (UTC)", scale=alt.Scale(domain=(23, 0))),
                    tooltip=[alt.Tooltip('current_time:Q', title='Current Time', format='.2f')]
                )

                # Combine map and vertical line
                chart = alt.layer(map_chart, time_line).properties(
                    height=400, width=800, background='#171717',
                    padding={"top": 0, "bottom": 0, "left": 10, "right": 10}
                ).configure_view(
                    stroke=None

                )

                # Display chart
                st.altair_chart(chart, use_container_width=True)

        with col2:
            with tile("clock", 460):
                st.markdown("Clock")

if __name__ == "__main__":
    DashboardPage()
