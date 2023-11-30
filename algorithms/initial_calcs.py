import pandas as pd
from datetime import date

df = pd.read_csv('QC_Production_timelines_ (3).csv')
# df['Due Date'] = pd.to_datetime(df['Due Date']).dt.date  
# df['Completed At'] = pd.to_datetime(df['Completed At']).dt.date
# due_date = df['Due Date']
# completion_date = df['Completed At']
# da_diff = due_date[0] - completion_date[4]


# print(da_diff.days)

#Checks for all events completed late in csv
def late_checker(df):

    # Change the due and completion date columns into datetime objects
    df['Due Date'] = pd.to_datetime(df['Due Date'])
    df['Completed At'] = pd.to_datetime(df['Completed At'])

    for index, row in df.iterrows():
        # variables for the if statement 
        due_date = row['Due Date']
        completion_date = row['Completed At']

        if due_date < completion_date:
            da_diff = completion_date - due_date
            print(f"The {row['Name']} event was late by { da_diff.days } day(s). Oh no!")

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

def in_progress(df):
    df['Start Date'] = pd.to_datetime(df['Start Date'])
    today = pd.to_datetime(date.today())
    
    for index, row in df.iterrows():
        if row['Start Date'] <= today and pd.isnull(row['Completed At']):
            print(f"The {row['Section/Column']} {row['Name']} event is in progress")


# # The is the show function for all events. Don't touch or you'll get spankies. 
def showall():
    print('-------------------------------------------------------------------------------------------------')
    print('EARLY')
    print('')
    early_checker(df)
    print('')
    print('#################################################################################################')
    print('')
    print('-------------------------------------------------------------------------------------------------')
    print('LATE')
    print('')
    late_checker(df)
    print('')
    print('#################################################################################################')
    print('')
    print('-------------------------------------------------------------------------------------------------')
    print('ON TIME')
    print('')
    on_time_checker(df)
