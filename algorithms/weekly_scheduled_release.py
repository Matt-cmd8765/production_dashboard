import pandas as pd
from datetime import date

# for testing fucntion
df = pd.read_csv('QC_Production_timelines_ (3).csv')

def release(df):
    data = []
    df['Due Date'] = pd.to_datetime(df['Due Date'])
    today = pd.to_datetime(date.today())
    current_week_num = today.isocalendar()[1]
    print(type(df['Due Date']))
    for index, row in df.iterrows():
        if row['Section/Column'] == 'Product Release' and row['Due Date'].isocalendar().week == current_week_num:
            data.append([row['Name'], row['Due Date']])
            print(f"The {row['Name']} release is scheduled for {row['Due Date']}")
    return data

release(df)
