import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from PIL import Image

# Define the reference date
reference_date = datetime(1950, 1, 1)

# Convert date to numeric
def date_to_numeric(date_obj, reference_date):
    if pd.isna(date_obj):
        return None
    return (date_obj - reference_date).days

# Load and prepare the CSV data
csv_file_path = '/Users/nir.chodorov/Downloads/CSV points - Jawhar.csv'
df = pd.read_csv(csv_file_path, header=None, names=['time', 'x', 'y', 'z'])

# Convert the 'time' column to datetime and then to numeric
df['time'] = pd.to_datetime(df['time'], format='%d/%m/%Y').apply(lambda x: date_to_numeric(x, reference_date))

# Ensure data types are correct
df = df.astype({'x': 'float', 'y': 'float', 'time': 'float'})

# Load the map image
map_image_path = '/Users/nir.chodorov/Downloads/600x600.png'  # Update with the path to your image
map_image = Image.open(map_image_path)

# Convert image to numpy array and normalize
map_array = np.array(map_image)
map_array = map_array / 255.0  # Normalize pixel values to range [0, 1] if needed

# Get map dimensions
map_height, map_width, _ = map_array.shape

# Create a grid for the surface
x = np.linspace(df['x'].min(), df['x'].max(), map_width)
y = np.linspace(df['y'].min(), df['y'].max(), map_height)
X, Y = np.meshgrid(x, y)
Z = np.zeros_like(X)  # Adjust Z based on your specific needs

# Create the 3D plot
fig = go.Figure()

# Add the surface map layer
fig.add_surface(
    x=X,
    y=Y,
    z=Z,
    surfacecolor=np.flipud(map_array[:, :, 0]),  # Use one channel or a custom approach
    colorscale='Viridis',  # Change as needed
    showscale=True  # Show color scale for debugging
)

# Add the 3D scatter plot
fig.add_trace(go.Scatter3d(
    x=df['x'],
    y=df['y'],
    z=df['time'],
    mode='markers',
    marker=dict(size=5, color=df['time'], colorscale='Viridis', colorbar=dict(title='Time (Days from Reference Date)')),
    name='3D Data Points'
))

# Update layout for 3D scatter plot
fig.update_layout(
    scene=dict(
        xaxis_title='Longitude',
        yaxis_title='Latitude',
        zaxis_title='Time (Days from Reference Date)'
    ),
    title='3D Space-Time Cube with Map Surface'
)

# Show the plot
fig.show()
