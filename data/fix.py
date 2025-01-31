import pandas as pd

# List of CSV files
csv_files = ['cv-unique-has-end-punct-sentences.csv', 'simple-wiki-unique-has-end-punct-sentences.csv']

# Column name you want to extract (assuming all files have the same column name)
column_name = 'sentence'

# Create an empty list to store the column data
combined_data = []

# Loop through each CSV file and extract the column data
for file in csv_files:
    df = pd.read_csv(file)
    if column_name in df.columns:
        combined_data.extend(df[column_name].tolist())  # Add column data to the list
    else:
        print(f"Column '{column_name}' not found in {file}")

# Create a new DataFrame from the combined data
combined_df = pd.DataFrame({column_name: combined_data})

# Save the combined DataFrame to a new CSV file
combined_df.to_csv('output.csv', index=False)

print("CSV files have been successfully combined!")
