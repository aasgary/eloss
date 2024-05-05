import streamlit as st
import rasterio
from rasterio.transform import from_origin
from pyproj import Proj, Transformer

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
            st.write(f"Width: {dataset.width}, Height: {dataset.height}")  # Check raster dimensions

            x, y = latlon_to_xy(lat, lon, dataset)
            row, col = dataset.index(x, y)
            st.write(f"Row: {row}, Col: {col}")  # Output row and col to check bounds

            if (row >= 0 and row < dataset.height) and (col >= 0 and col < the dataset.width):
                value = dataset.read(1)[row, col]
                return value
            else:
                return "Latitude and Longitude are out of the raster bounds."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit widgets to accept inputs
st.title("Raster Value Extraction Tool")
raster_path = st.text_input("Enter the path to the raster file:", 'v2023_1_pga_475_rock_3min.tif')
latitude = st.number_input("Enter the latitude:", value=56.23)
longitude = st.number_input("Enter the longitude:", value=-117.29)

# Button to trigger raster value reading
if st.button('Get Raster Value'):
    value = get_raster_value(latitude, longitude, raster_path)
    st.write(f"The pixel value at latitude {latitude} and longitude {longitude} is {value}")
