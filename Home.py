import streamlit as st
import rasterio
from rasterio.transform import from_origin
from pyproj import Proj, Transformer
import folium
from folium.plugins import MarkerCluster

# Function to convert lat/lon to the coordinate system of the raster
def latlon_to_xy(lat, lon, dataset):
    transformer = Transformer.from_crs("epsg:4326", dataset.crs, always_xy=True)
    x, y = transformer.transform(lon, lat)
    return x, y

# Function to get the raster value at a specific lat/lon
def get_raster_value(lat, lon, raster_path):
    try:
        with rasterio.open(raster_path) as dataset:
            st.write(f"Raster CRS: {dataset.crs}")
            st.write(f"Width: {dataset.width}, Height: {dataset.height}")

            x, y = latlon_to_xy(lat, lon, dataset)
            row, col = dataset.index(x, y)
            st.write(f"Row: {row}, Col: {col}")

            if 0 <= row < dataset.height and 0 <= col < dataset.width:
                value = dataset.read(1)[row, col]
                return value
            else:
                return "Latitude and Longitude are out of the raster bounds."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to display the map with the marked location
def show_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=13)
    folium.Marker([lat, lon], tooltip='Click me!', popup='Coordinates').add_to(m)
    return m

# Streamlit interface setup
st.title("Raster Value and Location Viewer")

# User inputs
raster_path = st.text_input("Enter the path to the raster file:", 'https://drive.google.com/uc?export=download&id=1TXBKnsp7hbIChr8UWzqEgFq5QhP58YYs')
latitude = st.number_input("Enter latitude:", value=46.23)
longitude = st.number_input("Enter longitude:", value=-120.29)

if st.button('Get Raster Value and Show Location'):
    value = get_raster_value(latitude, longitude, raster_path)
    if isinstance(value, str):
        st.error(value)
    else:
        st.success(f"The pixel value at latitude {latitude} and longitude {longitude} is {value}")
        map_display = show_map(latitude, longitude)
        # Display the folium map in Streamlit
        map_html = map_display._repr_html_()
        st.components.v1.html(map_html, height=500)
