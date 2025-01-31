import pandas as pd
import string

# Define allowed characters (alphanumeric + punctuation)
allowed_chars = string.ascii_letters + string.digits + string.punctuation + ' '

# Function to remove ambiguous characters
def remove_ambiguous_chars(text):
    return ''.join([char for char in text if char in allowed_chars])

# Load the CSV file
df = pd.read_csv('output.csv')

# Assuming 'sentence' column contains the text
column_name = 'sentence'

# Clean the sentences by removing ambiguous characters
df[column_name] = df[column_name].apply(lambda x: remove_ambiguous_chars(str(x)))

# Save the cleaned DataFrame back to the same CSV file
df.to_csv('output.csv', index=False)

print("Ambiguous characters have been removed and the file has been updated.")
