from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import geopandas as gpd

reference_date = datetime(1000, 1, 1)

def date_to_numeric(date_obj, reference_date):
    if pd.isna(date_obj):
        return None
    return (date_obj - reference_date).days

def custom_date_parser(date_str):
    return datetime.strptime(date_str, '%d/%m/%Y')

# Step 1: Read the CSV file
csv_file_path = '/Users/nir.chodorov/Downloads/CSV points - Jawhar.csv'  # Replace with your actual file path
df = pd.read_csv(csv_file_path, header=None, names=['time', 'x', 'y', 'z'],
                 parse_dates=['time'], date_parser=custom_date_parser)

df['time'] = df['time'].apply(lambda x: date_to_numeric(x, reference_date))

# Ensure data types are correct
df = df.astype({'x': 'float', 'y': 'float', 'time': 'float'})

# Step 2: Create a GeoDataFrame from the coordinates
geometry = gpd.points_from_xy(df['x'], df['y'])
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Step 3: Set up the 3D plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Step 4: Plot the map as the base (assuming you have a map as GeoDataFrame)
# For demonstration, we'll just use the bounding box of your coordinates as the "map"
bbox = gdf.total_bounds  # [minx, miny, maxx, maxy]

# Create a rectangular base map using the bounding box
xs = [bbox[0], bbox[0], bbox[2], bbox[2], bbox[0]]
ys = [bbox[1], bbox[3], bbox[3], bbox[1], bbox[1]]
ax.plot(xs, ys, zs=0, color='gray', alpha=0.5)

# Step 5: Overlay the CSV data on the 3D plot
ax.scatter(df['x'], df['y'], df['time'], c='r', marker='o')

# Step 6: Customize the plot
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Z (Time or Altitude)')
ax.set_title('3D Plot with Coordinates Map Base')

# Show the plot
plt.show()
