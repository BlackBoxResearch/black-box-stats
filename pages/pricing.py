import streamlit as st
from static.elements import tile, gradient_tile

def PricingPage():
    with st.container(border=False):
        st.markdown(
            """
            <div style="text-align: center; font-size: 2rem; color: "#3c3c3c"; font-weight: "bold";>
                Plans for every level of ambition
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("")
        st.markdown("")

        col1, col2, col3, col4 = st.columns([1, 1, 3 ,1], vertical_alignment="center")
        col2.toggle("Annual", value=True)
        col3.info('''16% off annually. It's like 60 days free 😍''')


        plan1, plan2, plan3 = st.columns(3, vertical_alignment="bottom")

        with plan1:
            with tile(
                key="pricing-plan-1",
                height=500,
                border=True
            ):
                with st.container(height=400, border=False):
                    st.markdown(
                        """
                        <div style="text-align: center; font-size: 1.5rem; color: "#3c3c3c"; font-weight: "bold";>
                            Free
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        """
                        <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
                            <span style="font-size: 2.4rem; font-weight: bold; color: "#3c3c3c";">£0</span>
                            <span style="font-size: 0.8rem; color: grey; margin-top: -10px;">/ month</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown("")
                    st.markdown("")
                    st.button("Buy Now", key="plan-1-subscribe", icon=":material/task_alt:", type="secondary", use_container_width=True)
                    st.markdown(
                    """
                    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
                    <div style="display: flex; align-items: center; font-size: 1 rem; margin-top: 10px">
                        <span class="material-icons" style="font-size: 1.5rem; margin-right: 15px;">check</span>
                        <span>Benefit 1</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                    )
                    st.markdown(
                    """
                    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
                    <div style="display: flex; align-items: center; font-size: 1 rem; margin-top: 10px">
                        <span class="material-icons" style="font-size: 1.5rem; margin-right: 15px;">check</span>
                        <span>Benefit 2</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        with plan2:
            with tile(
                key="pricing-plan-2",
                height=500,
                border=True
            ):
                    st.markdown(
                        """
                        <div style="text-align: center; font-size: 1.5rem; color: "#3c3c3c"; font-weight: "bold";>
                            Plus
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        """
                        <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
                            <span style="font-size: 2.4rem; font-weight: bold; color: "#3c3c3c";">£19.99</span>
                            <span style="font-size: 0.8rem; color: grey; margin-top: -10px;">/ month</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown("")
                    st.markdown("")
                    st.button("Buy Now", key="plan-2-subscribe", icon=":material/task_alt:", type="secondary", use_container_width=True)
                    st.markdown(
                    """
                    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
                    <div style="display: flex; align-items: center; font-size: 1 rem; margin-top: 10px">
                        <span class="material-icons" style="font-size: 1.5rem; margin-right: 15px;">check</span>
                        <span>Benefit 1</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                    )
                    st.markdown(
                    """
                    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
                    <div style="display: flex; align-items: center; font-size: 1 rem; margin-top: 10px">
                        <span class="material-icons" style="font-size: 1.5rem; margin-right: 15px;">check</span>
                        <span>Benefit 2</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with plan3:
            with tile(
                key="pricing-plan-3",
                height=500,
                border=True
            ):
                    st.markdown(
                        """
                        <div style="text-align: center; font-size: 1.5rem; color: "#3c3c3c"; font-weight: "bold";>
                            Premium
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        """
                        <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
                            <span style="font-size: 2.4rem; font-weight: bold; color: "#3c3c3c";">£49.99</span>
                            <span style="font-size: 0.8rem; color: grey; margin-top: -10px;">/ month</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown("")
                    st.markdown("")
                    st.button("Buy Now", key="plan-3-subscribe", icon=":material/task_alt:", type="primary", use_container_width=True)
                    st.markdown(
                    """
                    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
                    <div style="display: flex; align-items: center; font-size: 1 rem; margin-top: 10px">
                        <span class="material-icons" style="font-size: 1.5rem; margin-right: 15px;">check</span>
                        <span>Benefit 1</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                    )
                    st.markdown(
                    """
                    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
                    <div style="display: flex; align-items: center; font-size: 1 rem; margin-top: 10px">
                        <span class="material-icons" style="font-size: 1.5rem; margin-right: 15px;">check</span>
                        <span>Benefit 2</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    PricingPage()
