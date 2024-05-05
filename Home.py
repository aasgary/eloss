
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
            print(f"Raster CRS: {dataset.crs}")
            print(f"Width: {dataset.width}, Height: {dataset.height}")  # Check raster dimensions

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

raster_path = 'canadapga4753min.tif'
latitude = 56.23
longitude = -117.29

value = get_raster_value(latitude, longitude, raster_path)
print(f"The pixel value at latitude {latitude} and longitude {longitude} is {value}")

# Show the map with the location
map_display = show_map(latitude, longitude)
map_display  # Display the map in the output cell



# Streamlit interface setup
st.title("Raster Value and Location Viewer")
raster_path = st.text_input("Enter the path to the raster file:", 'https://drive.google.com/file/d/1D2pASBmz3Q06d0vzY4o0cowRorTKqr-f/view?usp=drive_link')
latitude = st.number_input("Enter latitude:", value=45.79)
longitude = st.number_input("Enter longitude:", value=-74.0)
if st.button('Get Raster Value and Show Location'):
    value = get_raster_value(latitude, longitude, raster_path)
    if isinstance(value, str):
        st.error(value)
    else:
        st.success(f"The pixel value at latitude {latitude} and longitude {longitude} is {value}")
        show_location_on_map(latitude, longitude)
