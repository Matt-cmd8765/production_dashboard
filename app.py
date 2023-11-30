from dash import Dash, html, dcc, callback, Output, Input, dash_table
from dash.exceptions import PreventUpdate
import plotly.express as px
from datetime import date
import pandas as pd
from algorithms.functions import in_progress, release, overdue, ontime, weekly

df = pd.read_csv('./db/QC_Production_timelines.csv')

# Fucntions to determine what activities are currently in progress
data = in_progress(df)
release_data = release(df)
overdue_data = overdue(df)
on_time_data = ontime(df)
weekly_data = weekly(df)


# Transform the 2d data array from in_progress into dataframe
dataf = pd.DataFrame(data, columns = ['Team', 'Activity', 'Due Date'])
release_table = pd.DataFrame(release_data, columns=['Name', 'Due Date', 'Completion Date'])
overdue_table = pd.DataFrame(overdue_data, columns=['Name', 'Due Date', 'Days Overdue'])
weekly_table = pd.DataFrame(weekly_data, columns=['Name', 'Team', 'Completion Date'])

# Pie Chart
on_time_pie = pd.DataFrame(on_time_data, columns=['Team', 'On Time?'])
# only looking at late or on time. Does not account for team
pie = on_time_pie.groupby('On Time?').count()
names = ['Early', 'Late', 'On Time']
# You get team name and late or on-time as a 2d array here. Team has to be passed as the value
fig = px.pie(pie, values='Team', names=names)

# initialize app
app = Dash(__name__)

app.layout = html.Div([
    # In-progress table
    html.H1(children='In Progress', style={'textAlign':'left'}),
    dcc.Dropdown(id='dropdown-selection', options=[{'label':i, 'value':i} for i in dataf.Team.unique()], value=['QC','Formulation'], style={'width': '55%'}, multi=True),
    dash_table.DataTable(data=dataf.to_dict('records'),fill_width=False,id='in-progress-table'),
    
    # Release table
    html.Div([html.H2(children='Weekly Release'),
    dash_table.DataTable(data=release_table.to_dict('records'), fill_width=False)]),

    # Overdue Table
    html.Div([html.H2(children='OVERDUE'),
    dash_table.DataTable(data=overdue_table.to_dict('records'), fill_width=False)]),

    # Weekly Task Completion Table
    html.Div([html.H2(children='Weekly Task Completion'),
    dash_table.DataTable(data=weekly_table.to_dict('records'), fill_width=False)]),

    # Pie Chart
    html.H4('Late, on-time or early?'),
    dcc.Graph(figure=fig)
])


@callback(
    Output('in-progress-table', 'data'),
    [Input('dropdown-selection', 'value')]
)

#Update in-progress table
def update_table(value):
	new_df = dataf[(dataf['Team'].isin(value))]
	return new_df.to_dict('records')
    # for val in value:
    # dff = dataf[dataf.Team==value]
    # return dff.to_dict('records')

# def update_df(town):
# 	new_df = df1[(df1['region'].isin(town)]
# # def generate_chart(names):
#     df = on_time_pie # replace with your own data source
#     fig = px.pie(df, values=on_time_pie.groupby('On Time?').count(), names=names, hole=.3)
#     return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
