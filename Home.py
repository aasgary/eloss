import streamlit as st
import rasterio
from pyproj import Proj, Transformer
import folium

# Define the flood types and their corresponding raster paths

flood_rasters = {
    "Flood 25": "https://drive.google.com/uc?export=download&id=1iLEuzYRML8Kb9qrPnXZppEuQS0D-68gy",
    "Flood 50": "https://drive.google.com/uc?export=download&id=1z0ilA-WhpXa7-GhbC0jzGQiEiUS2yBXL",
    #// and so on for other links
}

#flood_rasters = {
    #"Flood 25": "https://drive.google.com/file/d/1iLEuzYRML8Kb9qrPnXZppEuQS0D-68gy/view?usp=drive_link",
   # "Flood 50": "https://drive.google.com/file/d/1z0ilA-WhpXa7-GhbC0jzGQiEiUS2yBXL/view?usp=drive_link",
    #"Flood 100": "https://drive.google.com/file/d/1F_Jg4lv0BIt-NMtOp1kDsQLZIvJyT4uc/view?usp=drive_link",
    #"Flood 150": "https://drive.google.com/file/d/1TiyhSUzzbpvl0uPePd2lOYyBKMNY7c-K/view?usp=drive_link",
    #"Flood 200": "https://drive.google.com/file/d/1t6phb3FNfo5IZUP8fDYU6ZaQvg5RZ9Nl/view?usp=drive_link",
#}

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
latitude = st.number_input("Enter latitude:", value=45.62298452259461)
longitude = st.number_input("Enter longitude:", value=-61.99323924873502)

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
