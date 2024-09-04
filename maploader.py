import pandas as pd
import plotly.graph_objects as go
import numpy as np
from PIL import Image
# Your coordinates data
data = {
    'date': [
        '01/06/1959', '13/10/1960', '01/03/1969', '01/06/1969', '01/06/1970',
        '01/06/1976', '01/07/1976', '01/11/1976', '01/12/1976', '01/02/1977', '01/01/1992'
    ],
    'latitude': [
        31.27251811, 34.03352744, 31.22721523, 30.0004391, 33.50965695,
        31.93086036, 33.50965695, 32.78728924, 31.93086036, 31.67266603, 30.0609486
    ],
    'longitude': [
        -4.282063949, -5.007251054, 29.95206684, 31.23453349, 36.29455082,
        34.87294231, 36.29455082, 35.53144877, 34.87294231, 34.5622463, 31.2436969
    ]
}
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
# Normalize the z-values to the range 1900 to 2000
df['normalized_year'] = 1900 + (df['date'].dt.year - 1900)  # Ensure values are in the range 1900-2000
# Load and process the map image
image_path = '/Users/nir.chodorov/Downloads/600x600.png'
img = Image.open(image_path)
img = img.convert('RGB')
data = np.array(img)
# Define grid based on the map image dimensions
lon_min, lon_max = -180, 180
lat_min, lat_max = -90, 90
# Reverse latitude for the image
lat_grid = np.linspace(lat_max, lat_min, data.shape[0])
lon_grid = np.linspace(lon_min, lon_max, data.shape[1])
lon_grid, lat_grid = np.meshgrid(lon_grid, lat_grid)
# Create the z-values (elevation) for the surface plot
z_surface = np.zeros_like(lon_grid)
# Convert the image data to a color scale that Plotly can use
colorscale = np.mean(data, axis=2) / 255  # Normalize image data for color scaling
# Create a 3D surface plot with color data from the image
fig = go.Figure()
fig.add_trace(go.Surface(
    x=lon_grid,
    y=lat_grid,
    z=z_surface,
    surfacecolor=colorscale,
    colorscale='Viridis',
    colorbar_title='Map Texture',
    showscale=False,  # Hide the color bar for the texture
    opacity=0.8
))
# Add 3D scatter plot for data points
fig.add_trace(go.Scatter3d(
    x=df['longitude'],
    y=df['latitude'],
    z=df['normalized_year'],
    mode='markers',
    marker=dict(size=8, color=df['normalized_year'], colorscale='Viridis', opacity=0.8),
    name="Data Points"
))
# Update layout
fig.update_layout(
    scene=dict(
        xaxis_title='Longitude',
        yaxis_title='Latitude',
        zaxis_title='Year',
        zaxis=dict(range=[1900, 2000]),  # Set the z-axis range from 1900 to 2000
        camera=dict(eye=dict(x=1.5, y=1.5, z=0.5)),
    ),
    height=800,
    width=1000,
    title='3D Surface with Map Texture and Data Points'
)
fig.show()
