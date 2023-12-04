import pandas as pd
from datetime import date
import plotly.express as px
import numpy as np
from algorithms.functions import ontime

df = pd.read_csv('./db/QC_Production_timelines.csv')

on_time_data = ontime(df)

# Pie Chart for late, on time or early tracking
on_time_pie = pd.DataFrame(on_time_data, columns=['Team', 'on_time'])
# only looking at late, on time or early. Does not account for team

qc_late = sum((on_time_pie.Team == 'QC') & (on_time_pie.on_time == 'late'))
qc_ontime = sum((on_time_pie.Team == 'QC') & (on_time_pie.on_time == 'on_time'))
qc_early = sum((on_time_pie.Team == 'QC') & (on_time_pie.on_time == 'early'))

dick = [['QC','late',qc_late],['QC','On Time', qc_ontime], ['QC', 'Early', qc_early]]

pid = pd.DataFrame(dick, columns=['Team', 'On Time?', 'Count'])
# pie = on_time_pie.groupby(['Team']).agg(
#     status=(on_time_pie.groupby('On Time?'), np.sum),
# )
# print(pie)
# names = ['Early', 'Late', 'On Time']
# # You gets team name and late or on-time as a 2d array here. Team has to be passed as the value
fig = px.pie(pid, values='Count', names='On Time?')

fig.show()
