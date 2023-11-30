import plotly.express as px

fig = px.pie(values = [20, 50, 37, 18],
             names = ['G1', 'G2', 'G3', 'G4'],
             title = "Pie chart title")

fig.show() 
