import pandas as pd

# Load the Excel file
df = pd.read_excel('export.xlsx')

# Drop the columns
df = df.drop(columns=['response', 'organizer', 'start', 'end'])

# Remove duplicates
df = df.drop_duplicates()

# Select rows where attendees is not equal to 1
df = df.query("attendees != 1")

# Select rows where recurring is not equal to no
df = df.query("recurring != 'no'")

# Drop the recurring column
df = df.drop(columns=['recurring'])

# Sort rows by cadence of recurring series

df = df.sort_values(by=["Every week ‒ Mon", "Every week ‒ Tues"])


# Create a new DataFrame with rows where attendees is equal to 2
new_df = df[df['attendees'] == 2]

# Create a new Excel writer
writer = pd.ExcelWriter('updated_file.xlsx', engine='openpyxl')

# Write the original DataFrame to the first sheet
df.to_excel(writer, index=False, sheet_name='Sheet1')

# Write the new DataFrame to the second sheet
new_df.to_excel(writer, index=False, sheet_name='1:1s')

# Save the excel file
writer.save()
