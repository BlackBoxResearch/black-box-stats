import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import altair as alt
import pandas as pd

primary_background = '#111111'
secondary_background = '#171717'
dark_text_color = '#171717'
light_text_color = '#E8E8E8'
color_1 = '#5A85F3' #Blue
color_2 = '#CDFFD8' #Green
border_color = '#3c3c3c'

def metric_tile(key, stat, value, height, type, border, tooltip):
    """
    Creates a stylable metric tile using a custom container in Streamlit.

    Args:
        key (str): Unique key for the tile.
        stat (str): The title or label of the metric.
        value (str): The value to display for the metric.
        height (int): Height of the container in pixels.
        type (str): primary (#171717 background), secondary (Gradient Background).
        border (bool): If True, adds a 1px solid border with the specified border color. If False, no border is applied.
    
    """

    if type == "primary":
        text_color = light_text_color

        with tile(key, height, border):
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

        with gradient_tile(key=key, height=height):
            st.markdown(
                f"""
                    <div style="line-height: 1.4;">
                        <p style="margin: 0; font-size: 0.75em; color: {text_color};">{stat}</p>
                        <p style="margin: 0; font-size: 1em; font-weight: bold; color: {text_color};">{value}</p>
                    </div>
                    """,
                unsafe_allow_html=True, help=tooltip
            )

def tile(key, height, border):
    """
    Creates a stylable container in the Streamlit app with a specified height, background color, and optional border.

    Parameters:
        key (str): A unique key to identify the container in the Streamlit layout.
        height (int): The height of the container in pixels.
        border (bool): If True, adds a 1px solid border with the specified border color. If False, no border is applied.
    
    Behavior:
        - The container will have a secondary background color and light text color.
        - Border is optionally applied based on the `border` parameter.
        - The height of the container is adjustable via the `height` parameter.
    
    Returns:
        Streamlit container object: The styled container that can be further populated with Streamlit elements.
    """
    border_style = f"1px solid {border_color};" if border else "none;"
    
    with stylable_container(
        key=key,
        css_styles=f'''
        {{
            background-color: {secondary_background};
            border-radius: 0.5rem;
            border: {border_style};
            padding: calc(1em - 1px);
            color: {light_text_color};
        }}
        '''
    ):
        return st.container(border=False, height=height)
    
def gradient_tile(key, height):
    """
    Creates a stylable container in the Streamlit app with a specified height and optional background color.

    Parameters:
        key (str): A unique key to identify the container in the Streamlit layout.
        height (int): The height of the container in pixels.
        fill (bool): If True, fills with gradient fill, if False, animated gradient 1px border.
    
    Behavior:
        - The container will have a secondary background color and light text color.
        - The height of the container is adjustable via the `height` parameter.
        - Fill is optionally applied based on the `fill` parameter.
    
    Returns:
        Streamlit container object: The styled container that can be further populated with Streamlit elements.
    """

    css_style = f'''
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

    with stylable_container(
        key=key,
        css_styles=css_style
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
                        background: linear-gradient(90deg, {color_1}, {color_2});
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
            padding: 15px; /* Adjust padding as needed */
            margin-bottom: 17px; /* Add vertical spacing between containers */
            border-radius: 8px; /* Rounded corners */
            background-color: {secondary_background}; /* Inner container background */
            color: {light_text_color}; /* Text color */
            z-index: 1;
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
            border-radius: 8px; /* Match the container's border-radius */
            padding: 1px; /* Border thickness */
            -webkit-mask: 
                linear-gradient(#fff 0 0) content-box, 
                linear-gradient(#fff 0 0);
            -webkit-mask-composite: destination-out;
            mask-composite: exclude;
            background-image: conic-gradient(from var(--angle), {color_1}, {color_2}, {color_1}); /* Smooth circular loop */
            z-index: -1; /* Place behind the content */
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
        with st.container():
            st.markdown(
                f"""
                <div class="animated-container">{content}</div>
                """,
                unsafe_allow_html=True
            )

def hover_container(key: str, content: str):
    """
    A function to create a hoverable container with custom content.

    Args:
        key (str): The container's unique key.
        content (str): The HTML content to display inside the container.
    """
    css_styles = f'''
        .gradient-container {{
            position: relative;
            padding: 15px; /* Adjust padding as needed */
            margin-bottom: 17px; /* Add vertical spacing between containers */
            border-radius: 8px; /* Rounded corners */
            background-color: {secondary_background}; /* Inner container background */
            color: {light_text_color}; /* Text color */
            transition: all 0.3s ease; /* Smooth transition for hover effects */
            z-index: 1;
            width: 100%;
        }}
        .gradient-container::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border-radius: 8px; /* Match the container's border-radius */
            padding: 1px; /* Border thickness */
            background: linear-gradient(to bottom right, {color_1}, {color_2}); /* Gradient border */
            -webkit-mask: 
                linear-gradient(#fff 0 0) content-box, 
                linear-gradient(#fff 0 0);
            -webkit-mask-composite: destination-out;
            mask-composite: exclude;
            z-index: -1; /* Place behind the content */
            transition: all 0.3s ease; /* Smooth transition for hover effects */
        }}
        .gradient-container:hover {{
            background-color: #1e1e1e; /* Slightly lighter background on hover */
            box-shadow: 20px 0 100px {color_1}40, -20px 0 100px {color_2}40;
        }}
    '''

    with stylable_container(key=key, css_styles=css_styles):
        st.markdown(
            f"""
            <div class="gradient-container">{content}</div>
            """,
            unsafe_allow_html=True
        )

def gradient_container(key: str, content: str):
    """
    A function to create an animated container with custom content.

    Args:
        key (str): The container's unique key.
        content (str): The HTML content to display inside the container.
    """
    css_styles = f'''
        .animated-container {{
            position: relative;
            padding: 15px; /* Adjust padding as needed */
            margin-bottom: 17px; /* Add vertical spacing between containers */
            border-radius: 8px; /* Rounded corners */
            background-color: {secondary_background}; /* Inner container background */
            color: {light_text_color}; /* Text color */
            z-index: 1;
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
            border-radius: 8px; /* Match the container's border-radius */
            padding: 1px; /* Border thickness */
            -webkit-mask: 
                linear-gradient(#fff 0 0) content-box, 
                linear-gradient(#fff 0 0);
            -webkit-mask-composite: destination-out;
            mask-composite: exclude;
            background-image: conic-gradient(from var(--angle), {color_1}, {color_2}, {color_1}); /* Smooth circular loop */
            z-index: -1; /* Place behind the content */
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
        with st.container():
            st.markdown(
                f"""
                <div class="animated-container">{content}</div>
                """,
                unsafe_allow_html=True
            )

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
