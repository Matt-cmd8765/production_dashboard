from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
from datetime import date
import pandas as pd
from algorithms.functions import in_progress, release, overdue, ontime, weekly, current_status

df = pd.read_csv('./db/QC_Production_timelines.csv')

# Fucntions to determine what activities are currently in progress
data = in_progress(df)
release_data = release(df)
overdue_data = overdue(df)
on_time_data = ontime(df)
weekly_data = weekly(df)
current_data = current_status(df)

# Transform the 2d data array from in_progress into dataframe
dataf = pd.DataFrame(data, columns = ['Team', 'Activity', 'Due Date'])
release_table = pd.DataFrame(release_data, columns=['Name', 'Due Date', 'Completion Date'])
overdue_table = pd.DataFrame(overdue_data, columns=['Name', 'Due Date', 'Days Overdue'])
weekly_table = pd.DataFrame(weekly_data, columns=['Name', 'Team', 'Completion Date'])

# Pie Chart for late, on time or early tracking
on_time_pie = pd.DataFrame(on_time_data, columns=['Team', 'On Time?'])
# only looking at late, on time or early. Does not account for team
pie = on_time_pie.groupby('On Time?').count()
names = ['Early', 'Late', 'On Time']
# You gets team name and late or on-time as a 2d array here. Team has to be passed as the value
fig = px.pie(pie, values='Team', names=names)

# Current Status Pie Chart
current_pie = pd.DataFrame(current_data, columns=['Name', 'Status'])
current_pi = current_pie.groupby('Status').count()
boob = ['Overdue', 'On Time']
current_fig = px.pie(current_pi, values='Name', names=boob)

# Bootstrap style sheets
external_stylesheets = [dbc.themes.GRID]

# initialize app
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dbc.Container([
    # SpeeDx Header
    dbc.Row([
            html.Div(id='background', children=[html.P(children='')],style={'background-image': 'url("/assets/speedx-master-logo.png")', 
                             'background-repeat': 'no-repeat',
                             'background-position': 'top center',
                             'background-color':'#CDF6FF',
                             'height':'150px',
                             'border-radius':'6px'
                             })
    ]),
  
    dbc.Row([
        # In Progress Table
        dbc.Col(html.Div(children=[
            html.H1(children='In Progress', style={'textAlign':'left'}),
            dcc.Checklist(id='check-list-selection', options=[{'label':i, 'value':i} for i in dataf.Team.unique()], value=['QC','Formulation','Assembly'], inline=True),
            dash_table.DataTable(data=dataf.to_dict('records'),id='in-progress-table')])),

        # Weekly Task Completion Table
        dbc.Col(html.Div(children=[     
            html.H1(children='Weekly Task Completion'),
            dcc.Checklist(id='task_completion_checklist', options=[{'label':i, 'value':i} for i in dataf.Team.unique()], value=['QC','Formulation','Assembly'], inline=True),
            dash_table.DataTable(data=weekly_table.to_dict('records'),id='task_completion_table')]))
    ]),

    # dbc.Row([
    #     dbc.Col(html.Div(children=[
              
    #     ]))
    # ])
])


#     html.Div(id='substancediv', children=[
#     # In-progress table
#     dbc.Row(
#         [
#         # Release table
#         html.H2(children='Weekly Release'),
#         dash_table.DataTable(data=release_table.to_dict('records')),
#         ])
#     # Overdue Table
#     html.H2(children='OVERDUE'),
#     dash_table.DataTable(data=overdue_table.to_dict('records'))])]),

#     # Weekly Task Completion Table
#     html.H2(children='Weekly Task Completion'),
#     dash_table.DataTable(data=weekly_table.to_dict('records')),

#     # Pie Chart
#     html.H4('Late, on-time or early?'),
#     dcc.Graph(figure=fig),

#     # Current Status Pie Chart
#     html.H4('Current Status'),
#     dcc.Graph(figure=current_fig)    
#     ],style={'display':'inline-block'})
# ])


@callback(
    [Output('in-progress-table', 'data'),
    Output('task_completion_table', 'data')],
    [Input('check-list-selection', 'value'),
     Input('task_completion_checklist', 'contents')]
)

#Update in-progress table
def update_table(value,contents):
	new_df = dataf[(dataf['Team'].isin(value))]
	return new_df.to_dict('records')

def update_other_table(valuetwo):
    new_df = weekly_table[(weekly_table['Team'].isin(valuetwo))]
    return new_df.to_dict('records')
#Update weekly progress table
# def update_df(town):
# 	new_df = df1[(df1['region'].isin(town)]
# # def generate_chart(names):
#     df = on_time_pie # replace with iyour own data source
#     fig = px.pie(df, values=on_time_pie.groupby('On Time?').count(), names=names, hole=.3)
#     return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
