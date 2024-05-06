import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("Split-panel Map")

with st.expander("See source code"):
    with st.echo():
        # Initialize the map
        m = leafmap.Map()

        # Define your WMS or tile layer URLs
        left_raster_url = "https://drive.google.com/file/d/18jUhSQhjEpdRGibaDDhUNWM0ZqiZnn3g/view?usp=drive_link"
        right_raster_url = "https://drive.google.com/uc?export=download&id=1z0ilA-WhpXa7-GhbC0jzGQiEiUS2yBXL"
       
        # Using custom rasters in the split map
        m.split_map(
            left_layer=left_raster_url, 
            right_layer=right_raster_url,
            left_name="Custom Left Layer",  # Optionally name your layers
            right_name="Custom Right Layer"
        )

        # Add legends or other map components as necessary
        m.add_legend(title="Custom Layer Legend", builtin_legend="ESA_WorldCover")

m.to_streamlit(height=700)
