import streamlit as st
import leafmap.foliumap as leafmap
import rasterio
from pyproj import Proj, Transformer
import folium
from geopy.geocoders import Nominatim

# Initialize the geolocator
geolocator = Nominatim(user_agent="geoapiExercises")

# Flood_rasters dictionary (already defined)

# Function to convert lat/lon to the coordinate system of the raster
def latlon_to_xy(lat, lon, dataset):
    transformer = Transformer.from_crs("epsg:4326", dataset.crs, always_xy=True)
    x, y = transformer.transform(lon, lat)
    return x, y

def get_raster_value(lat, lon, raster_path):
    try:
        with rasterio.open(raster_path) as dataset:
            st.write(f"Raster CRS: {dataset.crs}")
            st.write(f"Width: {dataset.width}, Height: {dataset.height}")
            x, y = latlon_to_xy(lat, lon, dataset)
            row, col = dataset.index(x, y)
            if 0 <= row < dataset.height and 0 <= col < dataset.width:
                value = dataset.read(1)[row, col]
                return value
            else:
                return "Latitude and Longitude are out of the raster bounds."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def show_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=13)
    folium.Marker([lat, lon], tooltip='Click me!', popup='Coordinates').add_to(m)
    return m

st.title("Flood Value and Location Viewer")

# User input for address
address = st.text_input("Enter an address:")

# Dropdown menu for flood type
selected_flood_type = st.selectbox("Select a Flood Type:", list(flood_rasters.keys()))
raster_path = flood_rasters[selected_flood_type]

if st.button('Get Flood Level Value and Show Location'):
    # Use geopy to geocode the address
    location = geolocator.geocode(address)
    if location:
        latitude, longitude = location.latitude, location.longitude
        st.write(f"Geocoded Latitude: {latitude}, Longitude: {longitude}")
        value = get_raster_value(latitude, longitude, raster_path)
        if isinstance(value, str):
            st.error(value)
        else:
            st.success(f"The flood level value at latitude {latitude} and longitude {longitude} is {value}")
            map_display = show_map(latitude, longitude)
            map_html = map_display._repr_html_()
            st.components.v1.html(map_html, height=500)
    else:
        st.error("Unable to geocode the address. Please try a different one.")
