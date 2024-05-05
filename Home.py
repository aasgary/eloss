import streamlit as st
import pydeck as pdk
import rasterio
from rasterio.transform import from_origin
from pyproj import Proj, Transformer

from rasterio.plot import show
import folium

def show_map(lat, lon, raster_url):
    # Use the correct raw URL for the TIFF file
    with rasterio.open(raster_url) as src:
        # Your existing logic for processing the raster file
        print(f"Raster CRS: {src.crs}")
        print(f"Width: {src.width}, Height: {src.height}")

        # Additional logic to handle coordinates, etc.

    # Example map setup with folium to show the point
    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker([lat, lon]).add_to(m)
    return m

# Use the direct raw GitHub URL
raster_url = 'https://raw.githubusercontent.com/aasgary/eloss/66d4d2304ca9a1c94751f88c81d214460323b1bf/canadapga4753min.tif'
latitude = 56.23
longitude = -117.29
map_display = show_map(latitude, longitude, raster_url)
map_display
