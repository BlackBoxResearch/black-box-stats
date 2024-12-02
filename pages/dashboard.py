import streamlit as st
import altair as alt
from static.elements import tile, metric_tile, promo_container, animated_container, hover_container, promo_container
import pandas as pd
import datetime as dt
import numpy as np
from utils.stats import get_account_trades, get_user_accounts, get_account_info

now = dt.datetime.now(dt.timezone.utc)  # Get current time in UTC
current_time = now.hour + now.minute / 60  # Convert to hour with decimal minutes

def DashboardPage():
    with st.container(border=False):
        first_name = st.session_state.get("first_name", "User")
        user_id = st.session_state.get("user_id", "User")

        # Get the list of account numbers for the user
        account_numbers = get_user_accounts(user_id)
        
        st.subheader(f"Welcome back, {first_name}!", anchor=False)
        st.caption("Some message.")
    
        st.markdown("")
        st.markdown("")

        # Sample data for trading accounts
        accounts_data = [
            {"Account Name": "Account 1", "Balance": 1500, "Performance": np.random.randn(30).cumsum()},
            {"Account Name": "Account 2", "Balance": 2500, "Performance": np.random.randn(30).cumsum()},
            {"Account Name": "Account 3", "Balance": 1200, "Performance": np.random.randn(30).cumsum()},
            {"Account Name": "Account 4", "Balance": 3100, "Performance": np.random.randn(30).cumsum()},
        ]

        # Sample data for systems
        systems_data = [
            {
                "System Name": "System A",
                "Net Gain (%)": round(np.random.uniform(-10, 50), 2),  # Random net gain percentage
                "Performance": np.random.randn(30).cumsum(),
                "Black Box Score": np.random.randint(60, 100),  # Score out of 100
                "Published": np.random.choice(["Yes", "No"]),  # Published status
            },
            {
                "System Name": "System B",
                "Net Gain (%)": round(np.random.uniform(-10, 50), 2),
                "Performance": np.random.randn(30).cumsum(),
                "Black Box Score": np.random.randint(60, 100),
                "Published": np.random.choice(["Yes", "No"]),
            },
            {
                "System Name": "System C",
                "Net Gain (%)": round(np.random.uniform(-10, 50), 2),
                "Performance": np.random.randn(30).cumsum(),
                "Black Box Score": np.random.randint(60, 100),
                "Published": np.random.choice(["Yes", "No"]),
            },
            {
                "System Name": "System D",
                "Net Gain (%)": round(np.random.uniform(-10, 50), 2),
                "Performance": np.random.randn(30).cumsum(),
                "Black Box Score": np.random.randint(60, 100),
                "Published": np.random.choice(["Yes", "No"]),
            },
        ]

        col1, col2, col3, col4 = st.columns(4, vertical_alignment="bottom")

        with col1:
            promo_container(
                key="dashboard_plan_card", 
                content=f"""
                    <div style="line-height: 1.44;">
                        <p style="margin: 0; font-size: 0.75em; color: #878884;">Plan</p>
                        <p style="margin: 0; font-size: 1em; font-weight: bold; color: #E8E8E8;">Premium ✨</p>
                    </div>
                    """
                )

        with col2:
            metric_tile(
                key="dashboard_stat_1", 
                stat="Linked Accounts", 
                value="3 of 10", 
                height=40, 
                type="primary",
                border=True,
                tooltip=None
                )

        with col3:
            metric_tile(
                key="dashboard_stat_2", 
                stat="Member Since", 
                value="1st Jan 2024", 
                height=40, 
                type="primary",
                border=True,
                tooltip=None
                )

        with col4:
            metric_tile(
                key="dashboard_stat_3", 
                stat="Trader Rank", 
                value="#1340", 
                height=40, 
                type="primary",
                border=True,
                tooltip=None
                )
        
        st.divider()
        st.markdown("**My Accounts**")

        # Convert data into a pandas DataFrame
        df = pd.DataFrame(accounts_data)
        systems_df = pd.DataFrame(systems_data)

        # Displaying the table with sparklines
        st.dataframe(
            df,
            column_config={
                "Account Name": "Trading Account",
                "Balance": st.column_config.NumberColumn(
                    "Balance ($)", 
                    format="$%d"
                ),
                "Performance": st.column_config.AreaChartColumn(
                    "Performance Sparkline",
                    y_min=df["Performance"].apply(lambda x: min(x)).min(),
                    y_max=df["Performance"].apply(lambda x: max(x)).max(),
                ),
            },
            hide_index=True, use_container_width=True
        )

        st.divider()
        st.markdown("**My Systems**")

        # Displaying the table for Systems
        st.dataframe(
            systems_df,
            column_config={
                "System Name": "Portfolio System",
                "Net Gain (%)": st.column_config.NumberColumn(
                    "Net Gain (%)", 
                    format="%.2f%%"
                ),
                "Performance": st.column_config.AreaChartColumn(
                    "Performance Sparkline",
                    y_min=systems_df["Performance"].apply(lambda x: min(x)).min(),
                    y_max=systems_df["Performance"].apply(lambda x: max(x)).max(),
                ),
                "Black Box Score": st.column_config.ProgressColumn(
                    "Black Box Score",
                    format="%d",
                    help="The Black Box Score rates the portfolio based on historical performance and risk metrics.",
                ),
                "Published": st.column_config.TextColumn(
                    "Published",
                    help="Indicates whether the system is publicly available to subscribe to."
                ),
            },
            hide_index=True, use_container_width=True
        )


        # Define the HTML and JavaScript for the Chart.js chart
        chart_code = """
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
        <canvas id="myChart" width="400" height="150"></canvas>
        <script>
            let width, height, gradient;
            function getGradient(ctx, chartArea) {
                const chartWidth = chartArea.right - chartArea.left;
                const chartHeight = chartArea.bottom - chartArea.top;
                if (!gradient || width !== chartWidth || height !== chartHeight) {
                    width = chartWidth;
                    height = chartHeight;
                    gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
                    gradient.addColorStop(0, '#5A85F3');
                    gradient.addColorStop(1, '#CDFFD8');
                }
                return gradient;
            }

            const ctx = document.getElementById('myChart').getContext('2d');

            const chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
                    datasets: [{
                        label: 'Dataset',
                        data: [65, 59, 80, 81, 56, 55, 40],
                        fill: false,
                        borderColor: function(context) {
                            const { chart } = context;
                            const { ctx, chartArea } = chart;
                            if (!chartArea) {
                                return null;
                            }
                            return getGradient(ctx, chartArea);
                        },
                        tension: 0.4,
                        pointRadius: 0, // Remove data points
                        borderWidth: 1 // Set line width to 1px
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false // Remove legend
                        }
                    },
                    scales: {
                        x: {
                            display: true
                        },
                        y: {
                            display: true
                        }
                    }
                },
                plugins: ['glow'] // Activate the glow plugin
            });
        </script>
        </body>
        </html>
        """

        # Embed the HTML in Streamlit
        with tile("performance_chart", height=300, border=True):
            st.markdown("**Performance Chart**")
            st.components.v1.html(chart_code, height=280)

if __name__ == "__main__":
    DashboardPage()
