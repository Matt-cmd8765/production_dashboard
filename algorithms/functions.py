import pandas as pd
from datetime import date

# DF FOR TESTING: 
# df = pd.read_csv('QC_Production_timelines.csv')

# Function to generate in progress table OK
def in_progress(df):
    data = []
    # Make the necessary datetime objects
    df['Start Date'] = pd.to_datetime(df['Start Date'])
    today = pd.to_datetime(date.today())
    
    for index, row in df.iterrows():
        if row['Start Date'] <= today and pd.isnull(row['Completed At']):
            if row['Section/Column'] == 'QC Incoming Test' or row['Section/Column'] == 'QC Quality Final Test':
                data.append(['QC', row['Name'], row['Due Date']])
            else:
                data.append([row['Section/Column'], row['Name'], row['Due Date']])
            # print(f"The {row['Section/Column']} {row['Name']} event is in progress due date is {row['Due Date']}")
    return data

# Function to generate release tables
def release(df):
    data = []
    df['Due Date'] = pd.to_datetime(df['Due Date']).dt.date
    df['Completed At'] = pd.to_datetime(df['Completed At']).dt.date
    today = pd.to_datetime(date.today())
    current_week_num = today.isocalendar()[1]
    # print(type(df['Due Date']))
    for index, row in df.iterrows():
        if row['Section/Column'] == 'Product Release' and pd.notnull(row['Completed At']) and row['Completed At'].isocalendar().week == current_week_num:
            due_date = row['Due Date']
            completion_date = row['Completed At']
            data.append([row['Name'], due_date, completion_date])
            # print(f"The {row['Name']} release was released on {row['Completed At']}")
    return data

# Function to generate upcoming release table
def upcoming_release(df):
    data = []
    df['Due Date'] = pd.to_datetime(df['Due Date']).dt.date
    # print(type(df['Due Date']))
    for index, row in df.iterrows():
        if row['Section/Column'] == 'Product Release' and pd.isnull(row['Completed At']):
            due_date = row['Due Date']
            data.append([row['Name'], due_date])
            # print(f"The {row['Name']} release was released on {row['Completed At']}")
    return data

def upcoming_component_release(df):
    data = []
    df['Due Date'] = pd.to_datetime(df['Due Date']).dt.date
    for index, row in df.iterrows():
        if row['Section/Column'] == 'Raw Material Release' and pd.isnull(row['Completed At']):
            due_date = row['Due Date']
            data.append([row['Name'], due_date])
    return data


# Function to generate Weekly task comlpetion table OK but has time
def weekly(df):
    data = []
    df['Due Date'] = pd.to_datetime(df['Due Date']).dt.date
    df['Completed At'] = pd.to_datetime(df['Completed At']).dt.date
    today = pd.to_datetime(date.today())
    current_week_num = today.isocalendar()[1]
    # print(type(df['Due Date']))
    for index, row in df.iterrows():
        if pd.notnull(row['Completed At']) and row['Section/Column'] != 'Product Release' and row['Completed At'].isocalendar().week == current_week_num:
            completion_date = row['Completed At']
            if row['Section/Column'] == 'QC Incoming Test' or row['Section/Column'] == 'QC Quality Final Test':
                data.append([row['Name'], 'QC', completion_date])
            else:
                data.append([row['Name'], row['Section/Column'], completion_date])
            # print(f"The {row['Name']} release is scheduled for {row['Due Date']}")
    return data


# Function to generate overdue table
def overdue(df):
    data = []
    df['Due Date'] = pd.to_datetime(df['Due Date'])
    df['Completed At'] = pd.to_datetime(df['Completed At'])
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
    df['Due Date'] = pd.to_datetime(df['Due Date'])
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
    df['Due Date'] = pd.to_datetime(df['Due Date'])
    df['Completed At'] = pd.to_datetime(df['Completed At'])

    for index, row in df.iterrows():
        # variables for the if statement 
        due_date = row['Due Date']
        completion_date = row['Completed At']

        if due_date < completion_date:
            if row['Section/Column'] == 'QC Incoming Test' or row['Section/Column'] == 'QC Quality Final Test':
                data.append(['QC', 'late'])
            else:
                data.append([row['Section/Column'],'late'])
        if due_date == completion_date:
            if row['Section/Column'] == 'QC Incoming Test' or row['Section/Column'] == 'QC Quality Final Test':
                data.append(['QC', 'on_time'])
            else:
                data.append([row['Section/Column'],'on_time'])
        if due_date > completion_date:
            if row['Section/Column'] == 'QC Incoming Test' or row['Section/Column'] == 'QC Quality Final Test':
                data.append(['QC', 'early'])
            else:
                data.append([row['Section/Column'],'early'])
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
            #print(f"The {row['Name']} event was early by { diff.days } day(s). Hooray!")

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
