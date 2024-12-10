import streamlit as st
from streamlit_elements import elements, mui, html

# Gradient colors
color_start = "#000000"  # Black
color_end = "#1a1a3b"  # Dark blue

def ProfilePage():
    with elements("new_element"):
        with mui.Container():
            mui.Box(
                children=[
                    # Text Section
                    mui.Grid(
                        container=True,
                        direction="column",
                        spacing=2,
                        alignItems="flex-start",
                        children=[
                            mui.Grid(
                                item=True,
                                children=[
                                    mui.Typography(
                                        "Fully licensed MetaTrader 5 experience",
                                        variant="h5",
                                        component="div",
                                        sx={
                                            "color": "white",
                                            "fontWeight": "bold",
                                        },
                                    ),
                                ],
                            ),
                            mui.Grid(
                                item=True,
                                children=[
                                    mui.Typography(
                                        "Trade with Finotive Markets, a licensed MetaQuotes partner",
                                        variant="subtitle1",
                                        sx={"color": "white"},
                                    ),
                                ],
                            ),
                            mui.Grid(
                                item=True,
                                children=[
                                    mui.Typography(
                                        "We have onboarded with a fully licensed brokerage to "
                                        "provide our traders with the most reliable and most popular "
                                        "trading platform in the industry—MetaTrader 5.",
                                        variant="body2",
                                        sx={"color": "white", "marginTop": "10px"},
                                    ),
                                ],
                            ),
                            mui.Grid(
                                item=True,
                                children=[
                                    mui.Typography(
                                        "Visit finotivemarkets.com →",
                                        variant="body2",
                                        sx={
                                            "color": "#4183c4",
                                            "marginTop": "10px",
                                            "cursor": "pointer",
                                        },
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                sx={
                    "width": "100%",  # Full width
                    "maxWidth": "800px",  # Limit the width
                    "margin": "1em auto",  # Center horizontally with vertical margin
                    "padding": "1em",
                    "background": f"linear-gradient(135deg, {color_start}, {color_end})",
                    "borderRadius": "1.5rem",  # Smooth edges
                },
            )

    with st.container(border=False):
        st.subheader("My Profile", anchor=False)






if __name__ == "__main__":
    ProfilePage()
