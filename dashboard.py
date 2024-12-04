# Install necessary packages if not already installed
# pip install dash plotly pandas

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.io as pio

# Set a colorful theme for all graphs
pio.templates.default = "plotly"  # Can also try "seaborn" for a different look

# Load data
file_path = 'processed_data magType.csv'
df = pd.read_csv(file_path)

# Ensure `df` contains predictions and trends
data = df

# Ensure the dataset has required columns
required_columns = {'year', 'date', 'mag', 'latitude', 'longitude'}
if not required_columns.issubset(data.columns):
    raise ValueError(f"The dataset is missing required columns: {required_columns - set(data.columns)}")

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Earthquake Insights Dashboard"

# Layout
app.layout = html.Div([
    html.H1("Earthquake Trends and Predictions", style={'textAlign': 'center', 'fontSize': '30px', 'color': '#333'}),
    
    # Dropdown for filtering by year
    dcc.Dropdown(
        id='year-filter',
        options=[{'label': year, 'value': year} for year in sorted(data['year'].unique())],
        value=2024,  # Default value set to 2024
        placeholder="Select Year",
        style={'width': '50%', 'margin': '0 auto', 'padding': '10px'}
    ),
    
    # Graph for magnitude trends
    html.Div([
        dcc.Graph(id='magnitude-trend-graph'),
    ], style={'padding': '20px'}),

    # Scatter map for geospatial data
    html.Div([
        dcc.Graph(id='seismic-activity-map'),
    ], style={'padding': '20px'}),
], style={'fontFamily': 'Arial', 'backgroundColor': '#f9f9f9', 'padding': '20px'})

# Callbacks for interactivity
@app.callback(
    [Output('magnitude-trend-graph', 'figure'),
     Output('seismic-activity-map', 'figure')],
    [Input('year-filter', 'value')]
)
def update_graphs(selected_year):
    # Filter data based on selected year
    filtered_data = data[data['year'] == selected_year] if selected_year else data
    
    # Line chart for magnitude trends
    trend_fig = px.line(
        filtered_data,
        x='date',
        y='mag',
        title=f'Magnitude Trends for {selected_year}',
        labels={'date': 'Date', 'mag': 'Magnitude'},
        template='plotly'  # Colorful theme
    )
    
    # Scatter map for seismic activity
    map_fig = px.scatter_geo(
        filtered_data,
        lat='latitude',
        lon='longitude',
        color='mag',
        size='mag',
        title=f'Seismic Activity Map for {selected_year}',
        projection='natural earth',
        template='plotly'  # Colorful theme
    )
    
    return trend_fig, map_fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
