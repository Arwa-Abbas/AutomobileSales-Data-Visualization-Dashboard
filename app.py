import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv("historical_automobile_sales.csv")

app = dash.Dash(__name__)
app.title = "Automobile Sales Dashboard"  # Task 2.1 - Title

# App Layout
app.layout = html.Div([
    
    # 2.1 Title
    html.H1("Automobile Sales Analysis Dashboard", style={'textAlign': 'center'}),
    
    # 2.2 Dropdown for selecting report type
    html.Div([
        html.Label("Select Report Type", style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='report-type',
            options=[
                {'label': 'Recession Report', 'value': 'recession'},
                {'label': 'Yearly Report', 'value': 'yearly'}
            ],
            value='recession',
            placeholder='Choose report type',
            style={'width': '50%'}
        )
    ], style={'padding': '20px'}),  # Task 2.2 - Dropdown

    # 2.3 Output division
    html.Div(id='output-div', className='output-container'),  # Task 2.3 - Output Div with id and className

    # 2.5 & 2.6 Graph display
    dcc.Graph(id='sales-graph')
])

# 2.4 Callback to update based on dropdown selection
@app.callback(
    Output('output-div', 'children'),
    Output('sales-graph', 'figure'),
    Input('report-type', 'value')
)
def update_output(selected_report):
    if selected_report == "recession":
        output_text = "You are viewing: Recession Period Statistics"
        
        # 2.5 Graph for recession
        df_filtered = df[df["Recession"] == True]
        fig = px.line(
            df_filtered,
            x="Year",
            y="Automobile_Sales",
            color="Vehicle_Type",
            title="Recession Report: Vehicle Sales Trends by Type"
        )
    else:
        output_text = "You are viewing: Yearly Statistics"

        # 2.6 Graph for yearly report
        df_yearly = df.groupby("Year")["Automobile_Sales"].sum().reset_index()
        fig = px.bar(
            df_yearly,
            x="Year",
            y="Automobile_Sales",
            title="Yearly Report: Total Automobile Sales"
        )

    return html.H3(output_text), fig

# Run server
if __name__ == '__main__':
    app.run(debug=True)

