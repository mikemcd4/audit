import csv
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, request, render_template

## Add flask script here & at bottom ##


# Load the CSV file into a dataframe
df = pd.read_csv('your_file.csv')

# Split the first row into columns
df.columns = df.iloc[0]
df = df[1:]

# Drop the "start" and "end" columns
df = df.drop(['start', 'end'], axis=1)

# Remove duplicates
df = df.drop_duplicates()

# Remove all rows with a value of "1" in the "attendees" column
df = df[df.attendees != 1]

# Remove all rows with a value of "no" in the "recurring" column
df = df[df.recurring != 'no']

# Move all rows that don't have a value of "yes" in the "recurring" column to a new file named "corrupt_data"
corrupt_data = df[df.recurring != 'yes']
corrupt_data.to_csv('corrupt_data.csv', index=False)

# Remove these rows from the original csv file
df = df[df.recurring == 'yes']

# Convert the csv file to an excel file named "cal_audit_tool"
df.to_excel('cal_audit_tool.xlsx', index=False)

# Sort the rows in the excel file based on how the value of the "recurrence" column starts
df = df.sort_values(by=['recurrence'], key=lambda x: (x.startswith('Every week'), x.startswith('Every 2 weeks'), x.startswith('Every 3 weeks'), x.startswith('Every 4 weeks'), x.startswith('Every month'), x.startswith('Every 2 months'), x.startswith('Every 3 months')))

# Create a new column at the end titled "Meeting expires within 30 days"
df['Meeting expires within 30 days'] = 'no'
df.loc[(df['recurrence end'] <= (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S%z')), 'Meeting expires within 30 days'] = 'yes'

# Add every row with a value of "2" in the attendees column to a new sheet in the excel file named "1 on 1s"
writer = pd.ExcelWriter('cal_audit_tool.xlsx', engine='openpyxl')
book = load_workbook('cal_audit_tool.xlsx')
writer.book = book
one_on_ones = df[df.attendees == 2]
one_on_ones.to_excel(writer, sheet_name='1 on 1s', index=False)

# add every row with a value of "ORGANIZER" in the "response" column to a new sheet
meetings_i_own = df[df.response == 'ORGANIZER'] 
meetings_i_own.to_excel(writer, sheet_name='Meetings I Own', index=False)

writer.save()
