# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
spacex_df.tail(10)
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                options=[
                    {'label': 'All Sites', 'value': 'ALL'},
                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                ],
                value='ALL',
                placeholder="Select a Launch Site here",
                searchable=True
                ),
                                html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                # Function decorator to specify function input and output
                             

                               html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    1000: '1000',
                                                    2000: '2000',
                                                    3000: '3000',
                                                    4000: '4000',
                                                    5000: '5000',
                                                    6000: '6000',
                                                    7000: '7000',
                                                    8000: '8000',
                                                    9000: '9000',
                                                    10000: '10000'},
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total success launches by site')
        return fig
    else: 
     # return the outcomes piechart for a selected site 
          site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
          data = site_df['class'].value_counts()
          fig = px.pie(filtered_df, values=[data[1],data[0]],
          #names='class',
          title=f'Total success launches for {entered_site}')
          return fig
    
        
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='payload-slider', component_property='value'),
              Input(component_id='site-dropdown', component_property='value')
              )
def get_scatter(payload_range, entered_site):
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_range[0], payload_range[1])]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category'
        )
        return fig
    else: 
     # return the outcomes piechart for a selected site 
          site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
          fig = px.scatter(site_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
          title=f'Scatter Plot for {entered_site}'
          )
          return fig

# Run the app
if __name__ == '__main__':
    app.run_server()


#Which site has the largest successful launches?
#KSC LC-39A has the largest number of launches of 41.7%

#Which site has the highest launch success rate?
#CCAFS SLC-40 has the highest success launch rate of 42.9%

#Which payload range(s) has the highest launch success rate?
#No payload and 1000kg payloads have highest success rate

#Which payload range(s) has the lowest launch success rate?
#7000kg and above have lowest success rates

#Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest launch success rate?
#Booster FT has the highest success rate