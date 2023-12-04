from dash import Dash, html, dcc, callback, Output, Input, dash_table, callback_context
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
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
on_time_pie = pd.DataFrame(on_time_data, columns=['Team', 'on_time'])

qc_late = sum((on_time_pie.Team == 'QC') & (on_time_pie.on_time == 'late'))
qc_ontime = sum((on_time_pie.Team == 'QC') & (on_time_pie.on_time == 'on_time'))
qc_early = sum((on_time_pie.Team == 'QC') & (on_time_pie.on_time == 'early'))
form_late = sum((on_time_pie.Team == 'Formulation') & (on_time_pie.on_time == 'late'))
form_ontime = sum((on_time_pie.Team == 'Formulation') & (on_time_pie.on_time == 'on_time'))
form_early = sum((on_time_pie.Team == 'Formulation') & (on_time_pie.on_time == 'early'))
asm_late = sum((on_time_pie.Team == 'Assembly') & (on_time_pie.on_time == 'late'))
asm_ontime = sum((on_time_pie.Team == 'Assembly') & (on_time_pie.on_time == 'on_time'))
asm_early = sum((on_time_pie.Team == 'Assembly') & (on_time_pie.on_time == 'early'))
pr_late = sum((on_time_pie.Team == 'Product Release') & (on_time_pie.on_time == 'late'))
pr_ontime = sum((on_time_pie.Team == 'Product Release') & (on_time_pie.on_time == 'on_time'))
pr_early = sum((on_time_pie.Team == 'Product Release') & (on_time_pie.on_time == 'early'))

seconddf = [['QC','Late',qc_late],['QC','On Time', qc_ontime], ['QC', 'Early', qc_early], 
            ['Formulation','Late',form_late],['Formulation','On Time', form_ontime], ['Formulation', 'Early', form_early], 
            ['Assembly','Late',asm_late],['Assebmly','On Time', asm_ontime], ['Assembly', 'Early', asm_early],
            ['Product Release','Late',pr_late],['Product Release','On Time', pr_ontime], ['Product Release', 'Early', pr_early]]

pie = pd.DataFrame(seconddf, columns=['Team', 'On Time?', 'Count'])
# print(pie.loc[pie['Team']==])
# only looking at late, on time or early. Does not account for team
# pie = on_time_pie.groupby('On Time?').count()
# names = ['Early', 'Late', 'On Time']
# # You gets team name and late or on-time as a 2d array here. Team has to be passed as the value
fig = px.pie(pie, values='Count', names='On Time?')

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
            dcc.Checklist(id='check-list-selection', options=[{'label':i, 'value':i} for i in ['QC','Formulation','Assembly']], value=['QC','Formulation','Assembly'], inline=True),
            dash_table.DataTable(data=dataf.to_dict('records'),id='in-progress-table')
            ])),

        # Weekly Task Completion Table
        dbc.Col(html.Div(children=[     
            html.H1(children='Weekly Task Completion'),
            dcc.Checklist(id='task_completion_checklist', options=[{'label':i, 'value':i} for i in ['Formulation','QC','Assembly']], value=['QC','Formulation','Assembly'], inline=True),
            dash_table.DataTable(data=weekly_table.to_dict('records'),id='task_completion_table')
            ]))
    ]),

    dbc.Row([
        # Weekly Release Table
        dbc.Col(html.Div(children=[
            html.H1(children='Weekly Release'),
            dash_table.DataTable(data=release_table.to_dict('records'))
            ])),
        
        # Overdue Table
        dbc.Col(html.Div(children=[
            html.H1(children='OVERDUE'),
            dash_table.DataTable(data=overdue_table.to_dict('records'))
        ]))
    ]),

    dbc.Row([
        # Piechart for late, on time or early?
        dbc.Col(html.Div(children=[
            html.H1('Late, on-time or early?'),
            dcc.Checklist(id='names', options=[{'label':i, 'value':i} for i in ['QC','Formulation','Assembly']], value=['QC','Formulation','Assembly'], inline=True),
            dcc.Graph(figure=fig, id='on-time-pie')
        ])),

        # Piechart for current status
        dbc.Col(html.Div(children=[
            html.H1('Current Status'),
            dcc.Graph(figure=current_fig) 
        ]))
    ])
])

@callback(
    Output('in-progress-table', 'data'),
    Input('check-list-selection', 'value')
)

#Update in-progress table
def update_table(value):
    new_df = dataf[(dataf['Team'].isin(value))]
    return new_df.to_dict('records')

@callback(
    Output('task_completion_table', 'data'),
    Input('task_completion_checklist', 'value')
)

#Update weekly completion table
def update_table(value):
    new_df = weekly_table[(weekly_table['Team'].isin(value))]
    return new_df.to_dict('records')

@callback(
    Output("on-time-pie", "figure"), 
    Input("names", "value")
)
def generate_chart(value):
    new_df = pie[(pie['Team'].isin(value))]
    print(new_df)
    fig = px.pie(new_df, values='Count', names='On Time?')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
