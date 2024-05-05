import rasterio
from rasterio.plot import show
from pyproj import Transformer
import folium
from folium import plugins
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np

# Function to convert lat/lon to the coordinate system of the raster
def latlon_to_xy(lat, lon, dataset):
    transformer = Transformer.from_crs("epsg:4326", dataset.crs, always_xy=True)
    x, y = transformer.transform(lon, lat)
    return x, y

# Function to get the raster value at a specific lat/lon
def get_raster_value(lat, lon, raster_path):
    try:
        with rasterio.open(raster_path) as dataset:
            print(f"Raster CRS: {dataset.crs}")
            print(f"Width: {dataset.width}, Height: {dataset.height}")

            x, y = latlon_to_xy(lat, lon, dataset)
            row, col = dataset.index(x, y)
            print(f"Row: {row}, Col: {col}")

            if (row >= 0 and row < dataset.height) and (col >= 0 and col < dataset.width):
                value = dataset.read(1)[row, col]
                return value
            else:
                return "Latitude and Longitude are out of the raster bounds."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to display the map with the marked location and raster overlay
def show_map(lat, lon, raster_path):
    m = folium.Map(location=[lat, lon], zoom_start=8)
    folium.Marker([lat, lon]).add_to(m)

    # Open the raster file and read the first band
    with rasterio.open(raster_path) as src:
        # Convert the raster data to an image
        fig, ax = plt.subplots()
        show(src, ax=ax)
        ax.set_title('Raster Overlay')
        ax.axis('off')
        img = BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0)
        img.seek(0)
        plt.close()

        # Create an ImageOverlay
        bounds = [[src.bounds.bottom, src.bounds.left], [src.bounds.top, src.bounds.right]]
        folium.raster_layers.ImageOverlay(
            image=img,
            bounds=bounds,
            opacity=0.6,
            interactive=True,
            cross_origin=False,
            zindex=1,
        ).add_to(m)

    return m

raster_path = 'canadapga4753min.tif'
latitude = 56.23
longitude = -117.29

value = get_raster_value(latitude, longitude, raster_path)
print(f"The pixel value at latitude {latitude} and longitude {longitude} is {value}")

# Show the map with the location and raster overlay
map_display = show_map(latitude, longitude, raster_path)
map_display  # Display the map in the output cell
