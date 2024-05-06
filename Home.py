import streamlit as st
import rasterio
from pyproj import Proj, Transformer
import folium
import streamlit.components as components

# Flood_rasters dictionary
flood_rasters = {
    "Flood 25": "https://drive.google.com/uc?export=download&id=1iLEuzYRML8Kb9qrPnXZppEuQS0D-68gy",
    "Flood 50": "https://drive.google.com/uc?export=download&id=1z0ilA-WhpXa7-GhbC0jzGQiEiUS2yBXL",
    "Flood 100": "https://drive.google.com/uc?export=download&id=1Z8pIbnNmz7fpH0Ecm2wqU8ayUo5Zf4E_",
    "Flood 150": "https://drive.google.com/uc?export=download&id=18RcZJlZzvgc_cL1vKR1B6-9Ex3_xfV0-",
    "Flood 200": "https://drive.google.com/uc?export=download&id=16yAjxqvui4fNgcdzRZyzto3Q2B94J_qU",
}

def latlon_to_xy(lat, lon, dataset):
    transformer = Transformer.from_crs("epsg:4326", dataset.crs, always_xy=True)
    x, y = transformer.transform(lon, lat)
    return x, y

def get_raster_value(lat, lon, raster_path):
    try:
        with rasterio.open(raster_path) as dataset:
            x, y = latlon_to_xy(lat, lon, dataset)
            row, col = dataset.index(x, y)
            if 0 <= row < dataset.height and 0 <= col < dataset.width:
                return dataset.read(1)[row, col]
            else:
                return None  # Return None if out of bounds
    except Exception as e:
        return f"Error: {str(e)}"

def show_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=13)
    folium.Marker([lat, lon], tooltip='Click me!', popup='Coordinates').add_to(m)
    return m

# Streamlit app setup
st.title("Flood Level Value and Location Viewer")
latitude = st.number_input("Enter latitude:", value=44.379464761031706)
longitude = st.number_input("Enter longitude:", value=-64.51932009800133)

if st.button('Get Flood Level Values and Show Location'):
    results = {}
    for flood_type, path in flood_rasters.items():
        value = get_raster_value(latitude, longitude, path)
        results[flood_type] = value if value is not None else "Out of bounds"

    if results:
        for flood_type, value in results.items():
            st.write(f"{flood_type}: {value}")
        map_display = show_map(latitude, longitude)
        map_html = map_display._repr_html_()
        print(map_html)  # Check what is actually in map_html  
        st.components.v1.html(map_html, height=500)
    
