import pandas as pd
from datetime import date
import plotly.express as px
from algorithms.functions import ontime

df = pd.read_csv('./db/QC_Production_timelines_ (3).csv')

on_time_data = ontime(df)

on_time_pie = pd.DataFrame(on_time_data, columns=['Team', 'On Time?'])
# only looking at late or on time. Does not account for team
pie = on_time_pie.groupby('On Time?').count()
names = ['Late', 'On time']
# You get team name and late or on-time as a 2d array here. Team has to be passed as the value
fig = px.pie(pie, values='Team', names=names)
fig.show()
