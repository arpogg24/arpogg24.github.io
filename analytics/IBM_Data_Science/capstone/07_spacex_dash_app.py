# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# List of dictionaries of launch site options
launch_site_options = [{"label": "All Sites",    "value": "ALL"},
                       {"label": "CCAFS LC-40",  "value": "CCAFS LC-40"},
                       {"label": "VAFB SLC-4E",  "value": "VAFB SLC-4E"},
                       {"label": "KSC LC-39A",   "value": "KSC LC-39A"},
                       {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"}]

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center',
                                               'color': '#503D36',
                                               'font-size': 40}),
                                html.Div(dcc.Dropdown(
                                         id = "site-dropdown",
                                         options = launch_site_options,
                                         value = "ALL",
                                         placeholder = "Select launch site",
                                         searchable = True)),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                html.Div(dcc.RangeSlider(
                                         id = "payload-slider",
                                         min = 0, max = 10000, step = 1000,
                                         marks = {0: "0",
                                                  1000: "1000",
                                                  2000: "2000",
                                                  3000: "3000",
                                                  4000: "4000",
                                                  5000: "5000",
                                                  6000: "6000",
                                                  7000: "7000",
                                                  8000: "8000",
                                                  9000: "9000",
                                                  10000: "10000"},
                                         value = [min_payload, max_payload])),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

@app.callback(
    Output(component_id = "success-pie-chart", component_property = "figure"),
    Input(component_id = "site-dropdown", component_property = "value"))
def get_pie_chart(entered_site):
    if entered_site == "ALL":
        filtered_df = spacex_df.groupby("Launch Site")["class"].sum().reset_index()
        fig = px.pie(filtered_df,
                     values = "class",
                     names = "Launch Site",
                     title = "Successful Launches by Launch Site")
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        number_of_launches = len(filtered_df)
        number_of_successes = filtered_df["class"].sum()
        number_of_failures = number_of_launches - number_of_successes
        df_pie = pd.DataFrame({"count": [number_of_successes, number_of_failures]}, index = ["successes", "failures"])
        fig = px.pie(df_pie,
                     values = "count",
                     names = df_pie.index,
                     title = "Proportion of Failed and Successful Launches at Launch Site {}".format(entered_site))
    return fig

@app.callback(
    Output(component_id = "success-payload-scatter-chart", component_property = "figure"),
    [Input(component_id = "site-dropdown", component_property = "value"),
     Input(component_id = "payload-slider", component_property = "value")])
def get_scatter_plot(entered_site, payload_range):
    if entered_site == "ALL":
        filtered_df = spacex_df[["Payload Mass (kg)", "class", "Booster Version Category"]]
        fig = px.scatter(filtered_df,
                         x = "Payload Mass (kg)",
                         y = "class",
                         color = "Booster Version Category",
                         title = "Correlation Between Payload and Success for All Sites")
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        filtered_df = filtered_df[["Payload Mass (kg)", "class", "Booster Version Category"]]
        fig = px.scatter(filtered_df,
                         x = "Payload Mass (kg)",
                         y = "class",
                         color = "Booster Version Category",
                         title = "Correlation Between Payload and Success at Launch Site {}".format(entered_site))
    fig.update_xaxes(range = payload_range)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
