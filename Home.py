import streamlit as st
import rasterio
from pyproj import Proj, Transformer
import folium

# Define the flood types and their corresponding raster paths
flood_rasters = {
    "Flood 25": "https://drive.google.com/file/d/10-vw6_Gct-D0SlXzwIVrz1FUDI70ShB4/view?usp=drive_link",
    "Flood 50": "https://drive.google.com/file/d/1ccYo_JH8AAYbYM0DhTR3cm0jpZntRr-D/view?usp=drive_link",
    "Flood 100": "https://drive.google.com/file/d/1Ovrz51UX4aQ8lmxrJGVOtYGXusKyONN3/view?usp=drive_link",
    "Flood 150": "https://drive.google.com/file/d/1zEuTxmnb9RUtAkYfT-ytstd3dHre9aFi/view?usp=drive_link",
}

# Function definitions remain the same
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

# Streamlit interface setup
st.title("Raster Value and Location Viewer")

# Dropdown menu to select the flood type
selected_flood_type = st.selectbox("Select a Flood Type:", list(flood_rasters.keys()))

# Get the corresponding raster path
raster_path = flood_rasters[selected_flood_type]

# User inputs for latitude and longitude
latitude = st.number_input("Enter latitude:", value=46.23)
longitude = st.number_input("Enter longitude:", value=-120.29)

if st.button('Get Raster Value and Show Location'):
    value = get_raster_value(latitude, longitude, raster_path)
    if isinstance(value, str):
        st.error(value)
    else:
        st.success(f"The pixel value at latitude {latitude} and longitude {longitude} is {value}")
        map_display = show_map(latitude, longitude)
        map_html = map_display._repr_html_()
        st.components.v1.html(map_html, height=500)

        map_html = map_display._repr_html_()
        st.components.v1.html(map_html, height=500)
