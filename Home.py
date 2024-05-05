from rasterio.transform import from_origin
from pyproj import Proj, Transformer
import folium  # Import folium for mapping
import streamlit as st


# Function to convert lat/lon to the coordinate system of the raster
def latlon_to_xy(lat, lon, dataset):
    transformer = Transformer.from_crs("epsg:4326", dataset.crs, always_xy=True)
    x, y = transformer.transform(lon, lat)
    return x, y

# Function to get the raster value at a specific lat/lon
def get_raster_value(lat, lon, raster_path):
    try:
        with rasterio.open(raster_path) as dataset:
            print(f"Width: {dataset.width}, Height: {dataset.height}")  # Check raster dimensions
            st.write(f"Raster CRS: {dataset.crs}")
            st.write(f"Width: {dataset.width}, Height: {dataset.height}")
            st.write(f"Row: {row}, Col: {col}")
            x, y = latlon_to_xy(lat, lon, dataset)
            row, col = dataset.index(x, y)
            print(f"Row: {row}, Col: {col}")  # Output row and col to check bounds

            if (row >= 0 and row < dataset.height) and (col >= 0 and col < dataset.width):
                value = dataset.read(1)[row, col]
                return value
            else:
                return "Latitude and Longitude are out of the raster bounds."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to display the map with the marked location
def show_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=13)  # Create a map centered around the coordinates
    folium.Marker([lat, lon], tooltip='Click me!', popup='Coordinates').add_to(m)  # Add a marker for the location
    return m

raster_path = 'raster_path = 'https://drive.google.com/uc?export=download&id=1TXBKnsp7hbIChr8UWzqEgFq5QhP58YYs'
latitude = 46.23
longitude = -130.29

value = get_raster_value(latitude, longitude, raster_path)
print(f"The pixel value at latitude {latitude} and longitude {longitude} is {value}")

def show_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=13)
    folium.Marker([lat, lon], tooltip='Click me!', popup='Coordinates').add_to(m)
    
    # Convert map to HTML
    map_html = m._repr_html_()
    st.components.v1.html(map_html, height=500)

# And then call this in your Streamlit app
if st.button('Get Raster Value and Show Location'):
    value = get_raster_value(latitude, longitude, raster_path)
    if isinstance(value, str):
        st.error(value)
    else:
        st.success(f"The pixel value at latitude {latitude} and longitude {longitude} is {value}")
        show_map(latitude, longitude)
