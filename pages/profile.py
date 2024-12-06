from static.elements import gradient_text
import streamlit as st
from streamlit_elements import elements, mui, html, dashboard, nivo


def ProfilePage():
    with elements("dashboard"):
        st.subheader("My Profile", anchor=False)
        # You can create a draggable and resizable dashboard using
        # any element available in Streamlit Elements.


        # First, build a default layout for every element you want to include in your dashboard

        layout = [
            # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
            dashboard.Item("card-1", 0, 0, 1, 0.5, isDraggable=True, isResizable=False, moved=False),
            dashboard.Item("card-2", 1, 0, 1, 0.5, isDraggable=True, isResizable=False, moved=False),
            dashboard.Item("card-3", 2, 0, 1, 0.5, isDraggable=True, isResizable=False, moved=False),
            dashboard.Item("card-4", 3, 0, 1, 0.5, isDraggable=True, isResizable=False, moved=False),
                
            dashboard.Item("chart-1", 0, 1, 4, 1.5, isDraggable=True, isResizable=False, moved=False),

            dashboard.Item("chart-2", 0, 2, 2, 1.5, isDraggable=True, isResizable=False, moved=False),
            dashboard.Item("chart-3", 2, 2, 2, 1.5, isDraggable=True, isResizable=False, moved=False),

                ]

        # Next, create a dashboard layout using the 'with' syntax. It takes the layout
        # as first parameter, plus additional properties you can find in the GitHub links below.

        with dashboard.Grid(layout):#, onLayoutChange=handle_layout_change):
            mui.Box(
                "Some text in a styled box!",
                sx={
                    "bgcolor": "#171717",
                    "boxShadow": 1,
                    "borderRadius": 2,
                    "p": 2,
                    "width": "100%",
                    "padding": "18px 15px",
                    "marginBottom": "15px",
                    "fontFamily": "Segoe UI",
                    "fontSize": "0.75em",
                    "color": "#878884",
                    "justifyContent": "spaceBetween",
                    "flex": 1,
                    "display": "flex",
                    "boxSizing": "borderBox",
                    "alignItems": "top left",
                },
                key="card-1"
            )

            mui.Box(
                "Some text in a styled box!",
                sx={
                    "bgcolor": "#171717",
                    "boxShadow": 1,
                    "borderRadius": 2,
                    "p": 2,
                    "width": "100%",
                    "padding": "18px 15px",
                    "marginBottom": "15px",
                    "fontFamily": "Segoe UI",
                    "fontSize": "0.75em",
                    "color": "#878884",
                    "justifyContent": "spaceBetween",
                    "flex": 1,
                    "display": "flex",
                    "boxSizing": "borderBox",
                    "alignItems": "top left",
                },
                key="card-2"
            )

            mui.Box(
                "Some text in a styled box!",
                sx={
                    "bgcolor": "#171717",
                    "boxShadow": 1,
                    "borderRadius": 2,
                    "p": 2,
                    "width": "100%",
                    "padding": "18px 15px",
                    "marginBottom": "15px",
                    "fontFamily": "Segoe UI",
                    "fontSize": "0.75em",
                    "color": "#878884",
                    "justifyContent": "spaceBetween",
                    "flex": 1,
                    "display": "flex",
                    "boxSizing": "borderBox",
                    "alignItems": "top left",
                },
                key="card-3"
            )

            mui.Box(
                "Some text in a styled box!",
                sx={
                    "bgcolor": "#171717",
                    "boxShadow": 1,
                    "borderRadius": 2,
                    "p": 2,
                    "width": "100%",
                    "padding": "18px 15px",
                    "marginBottom": "15px",
                    "fontFamily": "Segoe UI",
                    "fontSize": "0.75em",
                    "color": "#878884",
                    "justifyContent": "spaceBetween",
                    "flex": 1,
                    "display": "flex",
                    "boxSizing": "borderBox",
                    "alignItems": "top left",
                },
                key="card-4"
            )

            mui.Box(
                "Chart!",
                sx={
                    "bgcolor": "#171717",
                    "boxShadow": 1,
                    "borderRadius": 2,
                    "p": 2,
                    "width": "100%",
                    "padding": "18px 15px",
                    "marginBottom": "15px",
                    "fontFamily": "Segoe UI",
                    "fontSize": "0.75em",
                    "color": "#878884",
                    "justifyContent": "spaceBetween",
                    "flex": 1,
                    "display": "flex",
                    "boxSizing": "borderBox",
                    "alignItems": "top left",
                },
                key="chart-1"
            )

            mui.Box(
                "Chart!",
                sx={
                    "bgcolor": "#171717",
                    "boxShadow": 1,
                    "borderRadius": 2,
                    "p": 2,
                    "width": "100%",
                    "padding": "18px 15px",
                    "marginBottom": "15px",
                    "fontFamily": "Segoe UI",
                    "fontSize": "0.75em",
                    "color": "#878884",
                    "justifyContent": "spaceBetween",
                    "flex": 1,
                    "display": "flex",
                    "boxSizing": "borderBox",
                    "alignItems": "top left",
                },
                key="chart-2"
            )

            with mui.Box(
                "Chart!",
                sx={
                    "bgcolor": "#171717",
                    "boxShadow": 1,
                    "borderRadius": 2,
                    "p": 2,
                    "width": "100%",
                    "padding": "18px 15px",
                    "marginBottom": "15px",
                    "fontFamily": "Segoe UI",
                    "fontSize": "0.75em",
                    "color": "#878884",
                    "justifyContent": "spaceBetween",
                    "flex": 1,
                    "display": "flex",
                    "boxSizing": "borderBox",
                    "alignItems": "top left",
                },
                key="chart-3"
            ):
                
                DATA = [
                    { "taste": "fruity", "chardonay": 93, "carmenere": 61, "syrah": 114 },
                    { "taste": "bitter", "chardonay": 91, "carmenere": 37, "syrah": 72 },
                    { "taste": "heavy", "chardonay": 56, "carmenere": 95, "syrah": 99 },
                    { "taste": "strong", "chardonay": 64, "carmenere": 90, "syrah": 30 },
                    { "taste": "sunny", "chardonay": 119, "carmenere": 94, "syrah": 103 },
    ]
                nivo.Radar(
                    data=DATA,
                    keys=[ "chardonay", "carmenere", "syrah" ],
                    indexBy="taste",
                    valueFormat=">-.2f",
                    margin={ "top": 70, "right": 80, "bottom": 40, "left": 80 },
                    borderColor={ "from": "color" },
                    gridLabelOffset=36,
                    dotSize=10,
                    dotColor={ "theme": "background" },
                    dotBorderWidth=2,
                    motionConfig="wobbly",
                    legends=[
                        {
                            "anchor": "top-left",
                            "direction": "column",
                            "translateX": -50,
                            "translateY": -40,
                            "itemWidth": 80,
                            "itemHeight": 20,
                            "itemTextColor": "#999",
                            "symbolSize": 12,
                            "symbolShape": "circle",
                            "effects": [
                                {
                                    "on": "hover",
                                    "style": {
                                        "itemTextColor": "#000"
                                    }
                                }
                            ]
                        }
                    ],
                    theme={
                        "background": "#FFFFFF",
                        "textColor": "#31333F",
                        "tooltip": {
                            "container": {
                                "background": "#FFFFFF",
                                "color": "#31333F",
                            }
                        }
                    }
                )



        def handle_layout_change(updated_layout):
            # You can save the layout in a file, or do anything you want with it.
            # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
            print(updated_layout)

if __name__ == "__main__":
    ProfilePage()
