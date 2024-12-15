import streamlit as st
from static.elements import tile

def PricingPage():
    with st.container(border=False):
        st.subheader("Pricing", anchor=False)

        plan1, plan2, plan3 = st.columns(3, vertical_alignment="top")

        with plan1:
            with tile(
                key="pricing-plan-1",
                height=500,
                border=True
            ):
                with st.container(height=400, border=False):
                    st.markdown("**Plan 1**")
                
                    st.divider()

                with st.container(height=100, border=False):
                    st.button("Subscribe", key="plan-1-subscribe", icon=":material/task_alt:", type="secondary", use_container_width=True)

        with plan2:
            with tile(
                key="pricing-plan-2",
                height=500,
                border=True
            ):
                st.markdown("Plan 2")

        with plan3:
            with tile(
                key="pricing-plan-3",
                height=500,
                border=True
            ):
                st.markdown("Plan 3")

if __name__ == "__main__":
    PricingPage()
