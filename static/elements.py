import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import altair as alt
import pandas as pd

primary_background = '#111111'
secondary_background = '#171717'
dark_text_color = '#171717'
light_text_color = '#ffffff'
color_1 = '#5A85F3' #fc4778 (pink) #fdbb2d (Yellow)
color_2 = '#59D2BA' #3952f5 (purple) #22c1c3 (Green)

def metric_tile(key, stat, value, height, type, tooltip):
    """
    Creates a stylable metric tile using a custom container in Streamlit.

    Args:
        key (str): Unique key for the tile.
        stat (str): The title or label of the metric.
        value (str): The value to display for the metric.
        height (int): Height of the container in pixels.
        type (str): primary (#171717 background), secondary (Gradient Background).
    """

    if type == "primary":
        text_color = light_text_color

        with tile(key, height):
            st.markdown(
                f"""
                    <div style="line-height: 1.4;">
                        <p style="margin: 0; font-size: 0.75em; color: {text_color};">{stat}</p>
                        <p style="margin: 0; font-size: 1em; font-weight: bold; color: {text_color};">{value}</p>
                    </div>
                    """,
                unsafe_allow_html=True, help=tooltip
            )

        
    elif type == "secondary":
        text_color = dark_text_color

        with gradient_tile(key, height):
            st.markdown(
                f"""
                    <div style="line-height: 1.4;">
                        <p style="margin: 0; font-size: 0.75em; color: {text_color};">{stat}</p>
                        <p style="margin: 0; font-size: 1em; font-weight: bold; color: {text_color};">{value}</p>
                    </div>
                    """,
                unsafe_allow_html=True
            )

def tile(key, height):
    with stylable_container(
        key=key,
        css_styles=f'''
        {{
            background-color: {secondary_background};
            border-radius: 0.5rem;
            padding: calc(1em - 1px);
            color: {light_text_color};
        }}
        '''
    ):
        return st.container(border=False, height=height)
    
def gradient_tile(key, height):
    with stylable_container(
        key="key",
        css_styles=f'''
        {{
            background: linear-gradient(135deg, {color_1}, {color_2});
            border-radius: 0.5rem;
            padding: 1em;
            color: {dark_text_color};
            display: flex;
            align-items: flex-start;
            justify-content: flex-start;
        }}
        '''
    ):
        return st.container(border=False, height=height)

def gradient_button(label, key, icon):
    """
    Creates a stylable button using a custom container in Streamlit.

    Args:
        label (str): Button text.
        key (str): Unique key for the tile.
        icon (str): Button material icon, e.g. ":material/check:".
    """
    with stylable_container(
            # border: 1px solid #434343;
            key="confirm_add_account_button",
            css_styles=f'''
                        button {{
                            background: linear-gradient(135deg, {color_1}, {color_2});
                            border-radius: 0.5rem;
                            color: {dark_text_color};
                        }}

                        button:active {{
                            transform: scale(0.98);
                        }}
                        ''',
    ):
        return st.button(label=label, key=key, icon=icon, use_container_width=True)

def gradient_text(text, font_size):
    """
    Creates text with a gradient colour in Streamlit.

    Args:
        text (str): Text to display.
        font_size (str): Text size, eg. 1em or 10px.
    """
    
    return st.markdown(
                    f'''
                    <h3 style="
                        font-size: {font_size};
                        background: linear-gradient(90deg, {color_1}, {color_2}, {color_1});
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        font-weight: bold;
                        text-align: left;">
                        {text}
                    </h3>
                    ''',
                    unsafe_allow_html=True
                )

def animated_container(key: str, content: str):
    """
    A function to create an animated container with custom content.

    Args:
        key (str): The container's unique key.
        content (str): The HTML content to display inside the container.
    """
    css_styles = f'''
        .animated-container {{
            position: relative;
            padding: 20px; /* Adjust padding as needed */
            margin-bottom: 20px; /* Add vertical spacing between containers */
            border-radius: 1rem; /* Rounded corners */
            background-color: {secondary_background}; /* Inner container background */
            color: {light_text_color}; /* Text color */
            z-index: 2;
            width: 100%;
        }}

        @property --angle {{
            syntax: "<angle>";
            initial-value: 0deg;
            inherits: false;
        }}

        .animated-container::after, .animated-container::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border-radius: 1rem; /* Match the container's border-radius */
            padding: 2px; /* Border thickness */
            -webkit-mask: 
                linear-gradient(#fff 0 0) content-box, 
                linear-gradient(#fff 0 0);
            -webkit-mask-composite: destination-out;
            mask-composite: exclude;
            background-image: conic-gradient(from var(--angle), {color_1}, {color_2}, {color_1}); /* Smooth circular loop */
            z-index: -2; /* Place behind the content */
            animation: spin 3s linear infinite;
        }}

        @keyframes spin {{
            from {{
                --angle: 0deg;
            }}
            to {{
                --angle: 360deg;
            }}
        }}
    '''

    with stylable_container(key=key, css_styles=css_styles):
        st.markdown(
            f"""
            <div class="animated-container">{content}</div>
            """,
            unsafe_allow_html=True
        )

# def hover_container(key: str, content: str, url=None):
#     """
#     A function to create a hoverable container with custom content.

#     Args:
#         key (str): The container's unique key.
#         content (str): The HTML content to display inside the container.
#     """
#     css_styles = f'''
#         .gradient-container {{
#             position: relative;
#             padding: 20px; /* Adjust padding as needed */
#             margin-bottom: 20px; /* Add vertical spacing between containers */
#             border-radius: 1rem; /* Rounded corners */
#             background-color: {secondary_background}; /* Inner container background */
#             color: {light_text_color}; /* Text color */
#             transition: all 0.3s ease; /* Smooth transition for hover effects */
#             z-index: 1;
#             width: 100%;
#         }}
#         .gradient-container::before {{
#             content: "";
#             position: absolute;
#             top: 0;
#             left: 0;
#             right: 0;
#             bottom: 0;
#             border-radius: 1rem; /* Match the container's border-radius */
#             padding: 2px; /* Border thickness */
#             background: linear-gradient(to bottom right, {color_1}, {color_2}); /* Gradient border */
#             -webkit-mask: 
#                 linear-gradient(#fff 0 0) content-box, 
#                 linear-gradient(#fff 0 0);
#             -webkit-mask-composite: destination-out;
#             mask-composite: exclude;
#             z-index: -1; /* Place behind the content */
#             transition: all 0.3s ease; /* Smooth transition for hover effects */
#         }}
#         .gradient-container:hover {{
#             background-color: #1e1e1e; /* Slightly lighter background on hover */
#             box-shadow: 20px 0 100px {color_1}40, -20px 0 100px {color_2}40;
#         }}
 

#     '''
#     if url:
#         with stylable_container(key=key, css_styles=css_styles):
#             st.markdown(
#                 f"""
#                 <a href=url style="text-decoration: none; color: inherit;">
#                     <div class="gradient-container">
#                         {content}
#                     </div>
#                 </a>
#                 """,
#                 unsafe_allow_html=True
#             )
#     else:
#         with stylable_container(key=key, css_styles=css_styles):
#             st.markdown(
#                 f"""
#                 <div class="gradient-container">{content}</div>
#                 """,
#                 unsafe_allow_html=True
#             )

# def markdown_container(key: str, content: str):
#     """
#     Create an animated container with a glowing effect.

#     Args:
#         key (str): A unique key for the container.
#         content (str): The HTML content to display inside the container.
#     """
#     css_styles = f'''
#         <style>
#             /* General container styling */
#             .animated-container-{key} {{
#                 position: relative;
#                 padding: 20px;
#                 margin-bottom: 20px;
#                 border-radius: 1rem;
#                 background-color: {secondary_background};
#                 color: {light_text_color};
#                 z-index: 2;
#                 width: 100%;
#             }}

#             /* Define custom property for animation */
#             @property --angle {{
#                 syntax: "<angle>";
#                 initial-value: 0deg;
#                 inherits: false;
#             }}

#             /* Glowing border styling */
#             .animated-container-{key}::before,
#             .animated-container-{key}::after {{
#                 content: "";
#                 position: absolute;
#                 top: 0;
#                 left: 0;
#                 right: 0;
#                 bottom: 0;
#                 border-radius: 1rem;
#                 padding: 2px;
#                 -webkit-mask: 
#                     linear-gradient(#fff 0 0) content-box, 
#                     linear-gradient(#fff 0 0);
#                 mask-composite: exclude;
#                 background-image: conic-gradient(from var(--angle), {color_1}, {color_2}, {color_1});
#                 z-index: -1; /* Place behind the content */
#                 animation: spin 3s linear infinite;
#             }}

#             /* Add blur and opacity effect for glowing */
#             .animated-container-{key}::after {{
#                 filter: blur(40px);
#                 opacity: 0.5;
#             }}

#             /* Keyframe animation */
#             @keyframes spin {{
#                 from {{
#                     --angle: 0deg;
#                 }}
#                 to {{
#                     --angle: 360deg;
#                 }}
#             }}
#         </style>
#     '''

#     # Inject CSS and create container
#     st.markdown(css_styles, unsafe_allow_html=True)
#     st.markdown(
#         f"""
#         <div class="animated-container-{key}">
#             {content}
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

# CHARTS

def line_chart(data, x, y, x_label, y_label, height=280):
    """
    Generate a line chart with a gradient fill.
    
    Parameters:
        data (pd.DataFrame): The DataFrame containing the data to plot.
        x (str): The column name for the x-axis.
        y (str): The column name for the y-axis.
        x_label (str): The label for the x-axis.
        y_label (str): The label for the y-axis.
        height (int): The height of the chart. Default is 280.
    
    Returns:
        alt.Chart: The Altair chart object.
    """
    # Ensure the x-axis column is interpreted as datetime
    data[x] = pd.to_datetime(data[x])
    
    # Create the main line chart with a gradient fill
    chart = alt.Chart(data).mark_area(
        line={'color': color_1},  # Line color
        color=alt.Gradient(  # Gradient fill with specified opacity
            gradient='linear',
            stops=[
                alt.GradientStop(color='rgba(148, 185, 255, 0.5)', offset=0),
                alt.GradientStop(color='rgba(148, 185, 255, 0)', offset=1)
            ],
            x1=1, x2=1, y1=1, y2=0
        ),
        interpolate='monotone'  # Smooth the line
    ).encode(
        x=alt.X(f'{x}:T', title=x_label),  # Specify temporal data type
        y=alt.Y(f'{y}:Q', title=y_label)  # Specify quantitative data type
    ).properties(
        height=height,  # Set the height of the chart
        background=secondary_background,  # Background color
        padding={"top": 10, "bottom": 10, "left": 10, "right": 10}
    ).configure_axis(
        grid=False  # Remove grid lines
    ).configure_view(
        strokeWidth=0  # Remove borders around the chart
    )
    
    return st.altair_chart(chart, use_container_width=True)

def scatter_chart(data, x, y, x_label, y_label, height=280):
    """
    Generate a scatter chart..
    
    Parameters:
        data (pd.DataFrame): The DataFrame containing the data to plot.
        x (str): The column name for the x-axis.
        y (str): The column name for the y-axis.
        x_label (str): The label for the x-axis.
        y_label (str): The label for the y-axis.
        height (int): The height of the chart. Default is 280.
    
    Returns:
        alt.Chart: The Altair chart object.
    """

    data[x]= pd.to_numeric(data[x], errors='coerce')
    
    # Create the main chart
    chart = alt.Chart(data).mark_circle(
                size=60,  # Size of the points
                color=color_1,  # Solid blue color
                opacity=0.7  # Set overall opacity of points
    ).encode(
        x=alt.X(f'{x}:Q', title=x_label),  # Specify quantitative data type
        y=alt.Y(f'{y}:Q', title=y_label)  # Specify quantitative data type
    ).properties(
        height=height,  # Set the height of the chart
        background=secondary_background,  # Background color
        padding={"top": 10, "bottom": 10, "left": 10, "right": 10}
    ).configure_axis(
        grid=False  # Remove grid lines
    ).configure_view(
        strokeWidth=0  # Remove borders around the chart
    )
    
    return st.altair_chart(chart, use_container_width=True)