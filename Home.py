import streamlit as st
import requests
import rasterio
from rasterio.transform import from_origin
from pyproj import Proj, Transformer

# Use the raw GitHub URL directly

tif_url = 'https://github.com/aasgary/eloss/blob/5e06cffb934252e7a2ca996ae6d49e14b97c9aaa/canadapga4753min.tif'

def get_raster_value(lat, lon, raster_url):
    try:
        # Use rasterio to open the remote file via HTTP
        with rasterio.open(raster_url) as dataset:
            st.write(f"Raster CRS: {dataset.crs}")
            st.write(f"Width: {dataset.width}, Height: {dataset.height}")
            
            # Assuming you have a function to convert lat/lon to raster coordinates
            # This should also handle any coordinate reference system transformations
            x, y = latlon_to_xy(lat, lon, dataset)
            row, col = dataset.index(x, y)
            st.write(f"Row: {row}, Col: {col}")

            # Ensure coordinates are within the image bounds
            if 0 <= row < dataset.height and 0 <= col < dataset.width:
                # Read the value from the raster
                value = dataset.read(1)[row, col]
                return f"The pixel value at latitude {latitude} and longitude {longitude} is {value}"
            else:
                return "Latitude and Longitude are out of the raster bounds."
    except Exception as e:
        return f"An error occurred: {str(e)}"
# Streamlit interface setup
latitude = st.number_input("Enter latitude:", value=56.23)
longitude = st.number_input("Enter longitude:", value=-117.29)
if st.button('Get Raster Value'):
    result = get_raster_value(latitude, longitude, tif_url)
    st.write(result)

if st.button('Get Raster Value'):
    value = get_raster_value(latitude, longitude, raster_path)
    st.write(f"The pixel value at latitude {latitude} and longitude {longitude} is {value}")
