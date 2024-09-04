import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

# Example dataset for two people
data = {
    'person': ['Al-Mu\'izz li-Din Allah'] * 5 + ['Al-Aziz Billah'] * 5 + ['Al-Hakim bi-Amr Allah'] * 6 + ['Al-Zahir li-I\'zaz Din Allah'] * 3 +
              ['Bard̲jjawan'] * 1 + ['Umm Mallal'] * 3 + ['Al-Mu\'izz ibn Badis'] * 4 +
              ['Sitt al-Mulk'] * 7 + ['Jawhar'] * 11 + ['Nicephorus I of Jerusalem'] * 5 +
              ['Orestes'] * 5 + ['Abu’l-Qāsim ʿAlī ibn Aḥmad al-Jarjarāʾī'] * 3 + ['Taqarrub'] * 3 +
              ['Umm walad Ruḳayya'] * 1 + ['Ḳāḍī Muḥammad b. al-Nuʿmān'] * 2,
    'date': [
        '26/09/1931', '05/08/1972', '11/11/1972', '11/06/1973', '18/12/1975', '11/05/1955', '09/08/1976', '14/10/1996',
        '01/06/1978', '11/06/1973', '13/08/1985', '15/10/1996', '16/10/1996', '01/01/2021', '12/02/2021', '13/02/2021',
        '20/06/2005', '28/03/2021', '01/06/2014', '14/10/1996', '30/05/2016', '24/06/2016', '01/06/2023', '19/01/2008',
        '13/05/2016', '24/06/2016', '29/10/2057', '12/10/1996', '13/10/1996', '14/10/1996', '05/02/2023', '31/08/1970',
        '01/11/1995', '01/12/1995', '01/06/1959', '13/10/1960', '01/03/1969', '01/06/1969', '01/06/1970', '01/06/1976',
        '01/07/1976', '01/11/1976', '01/12/1976', '01/02/1977', '01/01/1992', '01/04/2024', '01/03/2024', '01/02/2024',
        '01/11/2022', '01/11/2021', '01/06/1979', '01/06/1980', '01/06/1985', '01/06/1985', '01/06/2005', '01/01/1990',
        '01/06/2013', '01/06/2021', '01/11/1995', '01/06/1995', '01/06/2025', '01/06/2014', '12/10/1996', '13/10/1996'
    ],
    'latitude': [
        35.503684213503700, 35.677222, 30.05237529600630, 30.049742, 30.049742, 35.503684213503700, 30.049742,
        30.421667, 31.667286742388700, 30.049742,
        30.049742, 30.049742, 30.049742, 27.485828364246600, 30.049742, 30.02, 30.049742, 30.049742, 30.049409023657000,
        30.421667,
        35.503684213503700, 35.658056, 35.503684213503700, 36.683333, 35.503684213503700, 35.658056, 35.503684213503700,
        30.421667, 30.049058, 30.049409023657000, 30.049409023657000, 35.658056, 30.046667, 30.046667,
        31.27251810803510, 34.03352744285220, 31.227215225373900, 30.00043910089780, 33.50965695273520,
        31.9308603611233, 33.50965695273520, 32.78728923865440, 31.9308603611233, 31.672666026884100,
        30.060948596536200,
        30.049058, 34.436667, 36.204722, 41.008333, 41.005000, 30.049058, 41.915691825720000,
        41.915691825720000, 41.008333, 41.008333, 33.333333, 30.049409023657000, 30.049058,
        30.049409023657000, 30.049058, 30.049409023657000, 30.049058, 30.421667, 30.049058
    ],
    'longitude': [
        11.068751069718500, 10.100833, 31.12416518242670, 31.262152, 31.262152, 11.068751069718500, 31.262152,
        31.559167, 34.57332294910620, 31.262152,
        31.262152, 31.262152, 31.262152, 30.865170125515800, 31.262152, 31.3, 31.262152, 31.262152, 31.260956779530400,
        31.559167,
        11.068751069718500, 10.113889, 11.068751069718500, 10.15, 11.068751069718500, 10.113889, 11.068751069718500,
        31.559167, 31.262604, 31.260956779530400, 31.260956779530400, 10.113889, 31.276389, 31.276389,
        -4.282063948766740, -5.007251053510320, 29.95206684264980, 31.234533486067900, 36.29455082207190,
        34.872942306715300, 36.29455082207190, 35.531448772345700, 34.872942306715300, 34.562246297867000,
        31.243696901378300,
        31.262604, 35.834444, 36.181667, 28.98, 39.722500, 31.262604, 12.484499483880500, 12.484499483880500, 28.98,
        28.98,
        44.383333, 31.260956779530400, 31.262604, 31.260956779530400, 31.262604, 31.260956779530400, 31.262604,
        31.559167,
        31.262604
    ]
}

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

# Compute center and range for map centering
center_lat = df['latitude'].mean()
center_lon = df['longitude'].mean()
lon_range = df['longitude'].max() - df['longitude'].min()
lat_range = df['latitude'].max() - df['latitude'].min()

# Estimate zoom level based on range (simple heuristic)
zoom = 10 - int(max(lon_range, lat_range) // 5)

# Create the figure
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=('Interactive 2D Map', 'Space Time Cube'),
    specs=[[{'type': 'mapbox'}, {'type': 'scatter3d'}]],
    column_widths=[0.6, 0.4]  # Adjust column widths
)

colors = ['#94C58C','#0000FF','#0000CC','#BF40BF','#000099','#000066','#1A8828','#0A6921','#429B46','#000033','#FF5C00','#094F29','#71A73B','#0000FF','#75A818']
# Add the 2D map plot for each person
i = 0
for person, group in df.groupby('person'):
    fig.add_trace(
        go.Scattermapbox(
            lat=group['latitude'],
            lon=group['longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(size=9, color=colors[i]),
            text=group['date'].dt.year - 1000,
            name=f"{person} (2D)",
        ),
        row=1, col=1
    )
    i+=1

# Add the 3D scatter plot with lines connecting the dots for each person
# custom_colors = ['#607C3C', '#007F00', '#00CC00', '#B5E550', '#0000FF', '#00004C', '#6F00FF', '#FF4D00', '#0A2351', '#B9D9EB', '#00FF00', '#4C516D', '#007791', '#004C00', '#1877F2']# Different colors for each person
for i, (person, group) in enumerate(df.groupby('person')):
    fig.add_trace(
        go.Scatter3d(
            x=group['longitude'],
            y=group['latitude'],
            z=group['date'].dt.year - 1000,
            mode='lines+markers',  # Add 'lines' to connect the dots
            marker=dict(size=5, color=colors[i], opacity=0.8),
            # marker=dict(size=5, color=group['date'].dt.year, colorscale='Viridis', opacity=0.8),
            line=dict(color=colors[i], width=2),  # Customize line color and width
            name=f"{person} (3D)"
        ),
        row=1, col=2
    )

# Update mapbox layout for the 2D map
fig.update_layout(
    mapbox=dict(
        style="mapbox://styles/mapbox/light-v10",
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
        aspectratio=dict(x=1, y=1, z=0.5),  # Adjust aspect ratio for better spread
        domain={'x': [0.55, 1], 'y': [0, 1]},  # Adjust domain for better spread
        camera=dict(
            eye=dict(x=2, y=2, z=2)  # Adjust the camera's position
        )
    ),
    height=1000,  # Increase height
    width=1600,  # Increase width
    title="Network Map of Sitt al-Mulk: Familial, First and Second Degree Relationships"
)

# Show the figure
fig.show()

# Save the plot as an HTML file
pio.write_html(fig, '/Users/nir.chodorov/Downloads/plot.html', auto_open=True)
