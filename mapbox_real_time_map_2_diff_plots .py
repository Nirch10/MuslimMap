import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
# Example dataset
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

# Compute center and range
center_lat = df['latitude'].mean()
center_lon = df['longitude'].mean()
lon_range = df['longitude'].max() - df['longitude'].min()
lat_range = df['latitude'].max() - df['latitude'].min()

# Estimate zoom level based on range (simple heuristic)
zoom = 10 - int(max(lon_range, lat_range) // 5)

# Create the figure
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=('2D Map Base', '3D Scatter Plot'),
    specs=[[{'type': 'mapbox'}, {'type': 'scatter3d'}]]
)

# Add the 2D map plot
fig.add_trace(
    go.Scattermapbox(
        lat=df['latitude'],
        lon=df['longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(size=9, color=df['date'].dt.year, colorscale='Viridis'),
        text=df['date'].dt.year,
        name="2D Map",
    ),
    row=1, col=1
)

# Add the 3D scatter plot
fig.add_trace(
    go.Scatter3d(
        x=df['longitude'],
        y=df['latitude'],
        z=df['date'].dt.year - 1000,
        mode='markers',
        marker=dict(size=5, color=df['date'].dt.year, colorscale='Viridis', opacity=0.8),
        name="3D Scatter"
    ),
    row=1, col=2
)

# Update mapbox layout for the 2D map
fig.update_layout(
    mapbox=dict(
        style="mapbox://styles/mapbox/streets-v11",
        accesstoken="pk.eyJ1Ijoicm9zc3NwZSIsImEiOiJjbTA4Yjl4MHUxZ3VoMmpzaGN6N3gxc2I3In0.ZKDOiigoNNVjn5s9Ctd3Fw",  # Use your Mapbox access token here
        center=dict(lat=center_lat, lon=center_lon),
        zoom=zoom,
        bearing=0,
        pitch=0,
    ),
    scene=dict(
        xaxis_title='Longitude',
        yaxis_title='Latitude',
        zaxis_title='Year',
        domain={'x': [0.5, 1], 'y': [0, 1]}  # 3D scatter on the right half
    ),
    height=800,
    width=1000,
    title="Integrated 2D Map and 3D Scatter Plot"
)

# Show the figure
fig.show()
pio.write_html(fig, '/Users/nir.chodorov/Downloads/plot.html', auto_open=True)