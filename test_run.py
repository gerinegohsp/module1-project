import pandas as pd

# Read only the first 500 rows
df = pd.read_csv('SGJobData_cleaned.csv.gz', nrows=500)

print(df.shape)   # should show (500, number_of_columns)
print(df.head())  # preview first 5 rows
# Show all column names
print(df.columns)
