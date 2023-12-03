import pandas as pd
from datetime import date

# DF FOR TESTING: 
# df = pd.read_csv('./db/QC_Production_timelines.csv')

# Function to generate in progress table
def in_progress(df):
    data = []
    # Make the necessary datetime objects
    df['Start Date'] = pd.to_datetime(df['Start Date'], dayfirst=True)
    today = pd.to_datetime(date.today())
    
    for index, row in df.iterrows():
        if row['Start Date'] <= today and pd.isnull(row['Completed At']):
            data.append([row['Section/Column'], row['Name'], row['Due Date']])
            # print(f"The {row['Section/Column']} {row['Name']} event is in progress due date is {row['Due Date']}")
    return data

# Function to generate release tables
def release(df):
    data = []
    df['Due Date'] = pd.to_datetime(df['Due Date'], dayfirst=True)
    df['Completed At'] = pd.to_datetime(df['Completed At'], dayfirst=True)
    today = pd.to_datetime(date.today())
    current_week_num = today.isocalendar()[1]
    # print(type(df['Due Date']))
    for index, row in df.iterrows():
        if row['Section/Column'] == 'Product Release' and pd.notnull(row['Completed At']) and row['Completed At'].isocalendar().week == current_week_num:
            due_date = row['Due Date'].strftime("%d-%m-%Y")
            completion_date = row['Completed At'].strftime("%d-%m-%Y")
            data.append([row['Name'], due_date, completion_date])
            # print(f"The {row['Name']} release is scheduled for {row['Due Date']}")
    return data

# Function to generate Weekly task comlpetion table
def weekly(df):
    data = []
    df['Due Date'] = pd.to_datetime(df['Due Date'], dayfirst=True)
    df['Completed At'] = pd.to_datetime(df['Completed At'], dayfirst=True)
    today = pd.to_datetime(date.today())
    current_week_num = today.isocalendar()[1]
    # print(type(df['Due Date']))
    for index, row in df.iterrows():
        if pd.notnull(row['Completed At']) and row['Section/Column'] != 'Product Release' and row['Completed At'].isocalendar().week == current_week_num:
            completion_date = row['Completed At'].strftime("%d/%m/%Y")
            data.append([row['Name'], row['Section/Column'], completion_date])
            # print(f"The {row['Name']} release is scheduled for {row['Due Date']}")
    return data


# Function to generate overdue table
def overdue(df):
    data = []
    df['Due Date'] = pd.to_datetime(df['Due Date'], dayfirst=True)
    today = pd.to_datetime(date.today())
    for index, row in df.iterrows():
        if row['Due Date'] < today and pd.isnull(row['Completed At']):
            due_date = row['Due Date']
            difference = today - due_date
            data.append([row['Name'], due_date.strftime("%d-%m-%Y"), difference.days])
    return data

# Generate current status pie chart 
def current_status(df):
    data=[]
    df['Due Date'] = pd.to_datetime(df['Due Date'], dayfirst=True)
    today = pd.to_datetime(date.today())
    for index, row in df.iterrows():
        if row['Due Date'] < today and pd.isnull(row['Completed At']):
            data.append([row['Name'], 'Overdue'])
        if row['Due Date'] > today and pd.isnull(row['Completed At']):
            data.append([row['Name'], 'On Time'])
    return data

#Checks for all events completed late in csv
def ontime(df):
    data = []
    # Change the due and completion date columns into datetime objects
    df['Due Date'] = pd.to_datetime(df['Due Date'], dayfirst=True)
    df['Completed At'] = pd.to_datetime(df['Completed At'], dayfirst=True)

    for index, row in df.iterrows():
        # variables for the if statement 
        due_date = row['Due Date']
        completion_date = row['Completed At']

        if due_date < completion_date:
            data.append([row['Section/Column'],'late'])
        if due_date == completion_date:
            data.append([row['Section/Column'], 'on_time'])
        if due_date > completion_date:
            data.append([row['Section/Column'], 'early'])
    return data            


#Lists all events completed ahead of schedule
def early_checker(df):

    # Change the due and completion date columns into datetime objects
    df['Due Date'] = pd.to_datetime(df['Due Date'])
    df['Completed At'] = pd.to_datetime(df['Completed At'])

    for index, row in df.iterrows():
        # variables for the if statement 
        due_date = row['Due Date']
        completion_date = row['Completed At']

        if due_date > completion_date:
            diff = due_date - completion_date
            print(f"The {row['Name']} event was early by { diff.days } day(s). Hooray!")

def on_time_checker(df):

    # Change the due and completion date columns into datetime objects
    df['Due Date'] = pd.to_datetime(df['Due Date'])
    df['Completed At'] = pd.to_datetime(df['Completed At'])

    for index, row in df.iterrows():
        # variables for the if statement 
        due_date = row['Due Date']
        completion_date = row['Completed At']
        if due_date == completion_date:
            print(f"The {row['Section/Column']} {row['Name']} event was completed on time. Nice!")

