import streamlit as st
import pydeck as pdk
import rasterio
from rasterio.transform import from_origin
from pyproj import Proj, Transformer

# Function to convert lat/lon to the coordinate system of the raster
def latlon_to_xy(lat, lon, dataset):
    transformer = Transformer.from_crs("epsg:4326", dataset.crs, always_xy=True)
    x, y = transformer.transform(lon, lat)
    return x, y

import rasterio

import rasterio

# Correctly format the URL with /vsicurl/ if confirmed it's direct
def get_raster_value(lat, lon, raster_url):
    try:
        # Ensure URL is correctly prefixed for rasterio's remote capabilities
        raster_url_corrected = f'/vsicurl/{raster_url}'
        with rasterio.open(raster_url_corrected) as dataset:
            print(f"Raster CRS: {dataset.crs}")
            print(f"Width: {dataset.width}, Height: {dataset.height}")

            x, y = latlon_to_xy(lat, lon, dataset)
            row, col = dataset.index(x, y)
            print(f"Row: {row}, Col: {col}")

            if 0 <= row < dataset.height and 0 <= col < dataset.width:
                value = dataset.read(1)[row, col]
                return value
            else:
                return "Latitude and Longitude are out of the raster bounds."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Adjust your usage accordingly


# Adjust your usage accordingly


def show_location_on_map(lat, lon):
    # Define the map centered around the location
    map_view = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=lat,
            longitude=lon,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=[{'position': [lon, lat], 'size': 200}],
                get_position='position',
                get_color=[180, 0, 200, 140],
                get_radius='size',
            ),
        ],
    )
    st.pydeck_chart(map_view)

# Streamlit interface setup
st.title("Raster Value and Location Viewer")
raster_path = st.text_input("Enter the path to the raster file:", 'https://drive.google.com/file/d/18T1EeRtO6WEaIfmkFgQ3o7P4XTARWL7a/view?usp=drive_link')
latitude = st.number_input("Enter latitude:", value=56.23)
longitude = st.number_input("Enter longitude:", value=-117.29)

if st.button('Get Raster Value and Show Location'):
    value = get_raster_value(latitude, longitude, raster_path)
    if isinstance(value, str):
        st.error(value)
    else:
        st.success(f"The pixel value at latitude {latitude} and longitude {longitude} is {value}")
        show_location_on_map(latitude, longitude)
