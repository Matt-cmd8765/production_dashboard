from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
from datetime import date
import pandas as pd
from algorithms.functions import in_progress, release, overdue

df = pd.read_csv('./db/QC_Production_timelines_ (3).csv')

# Fucntion to determine what activities are currently in progress
data = in_progress(df)
release_data = release(df)
overdue_data = overdue(df)

# Transform the 2d data array from in_progress into dataframe
dataf = pd.DataFrame(data, columns = ['Team', 'Activity', 'Due Date'])
release_table = pd.DataFrame(release_data, columns=['Name', 'Due Date'])
overdue_table = pd.DataFrame(overdue_data, columns=['Name', 'Due Date', 'Days Overdue'])

app = Dash(__name__)

app.layout = html.Div([
    # Layout for in-progress table
    html.H1(children='In Progress', style={'textAlign':'left'}),
    dcc.Dropdown(dataf.Team.unique(), 'QC', id='dropdown-selection', style={'width': '55%'}),
    dash_table.DataTable(data=dataf.to_dict('records'),fill_width=False,id='in-progress-table'),
    
    # Release table
    html.Div([html.H2(children='Weekly Release'),
    dash_table.DataTable(data=release_table.to_dict('records'), fill_width=False)]),

    # Overdue Table
    html.Div([html.H2(children='OVERDUE'),
    dash_table.DataTable(data=overdue_table.to_dict('records'), fill_width=False)])
])

@callback(
    Output('in-progress-table', 'data'),
    Input('dropdown-selection', 'value')
)

#Update in-progress table
def update_table(value):
    dff = dataf[dataf.Team==value]
    return dff.to_dict('records')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)