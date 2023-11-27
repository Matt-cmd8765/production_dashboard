import pandas as pd
from datetime import date

# DF FOR TESTING: df = pd.read_csv('QC_Production_timelines_ (3).csv')

# Function to generate in progress table
def in_progress(df):
    data = []
    # Make the necessary datetime objects
    df['Start Date'] = pd.to_datetime(df['Start Date'])
    today = pd.to_datetime(date.today())
    
    for index, row in df.iterrows():
        if row['Start Date'] <= today and pd.isnull(row['Completed At']):
            data.append([row['Section/Column'], row['Name'], row['Due Date']])
            # print(f"The {row['Section/Column']} {row['Name']} event is in progress due date is {row['Due Date']}")
    return data

# Function to generate release tables
def release(df):
    data = []
    df['Due Date'] = pd.to_datetime(df['Due Date'])
    today = pd.to_datetime(date.today())
    current_week_num = today.isocalendar()[1]
    # print(type(df['Due Date']))
    for index, row in df.iterrows():
        if row['Section/Column'] == 'Product Release' and row['Due Date'].isocalendar().week == current_week_num:
            due_date = row['Due Date'].strftime("%d-%m-%Y")
            data.append([row['Name'], due_date])
            # print(f"The {row['Name']} release is scheduled for {row['Due Date']}")
    return data

# Function to generate overdue table
def overdue(df):
    data = []
    df['Due Date'] = pd.to_datetime(df['Due Date'])
    today = pd.to_datetime(date.today())
    for index, row in df.iterrows():
        if row['Due Date'] < today and pd.isnull(row['Completed At']):
            due_date = row['Due Date']
            difference = today - due_date
            data.append([row['Name'], due_date.strftime("%d-%m-%Y"), difference.days])
    return data