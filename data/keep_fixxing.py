import pandas as pd
import matplotlib.pyplot as plt

# Load the output.csv file
df = pd.read_csv('output.csv')

# Assuming 'sentence' column contains the text
column_name = 'sentence'

# Function to classify sentences based on the number of words
def classify_sentence_by_length(sentence):
    word_count = len(sentence.split())
    if word_count <= 11:
        return 'easy'
    elif word_count <= 20:
        return 'medium'
    else:
        return 'hard'

# Create a new column 'classification' based on the word count
df['classification'] = df[column_name].apply(classify_sentence_by_length)

# Save the new DataFrame with classifications to a new CSV file
df.to_csv('classified_output.csv', index=False)

print("The sentences have been classified and saved to 'classified_output.csv'.")

# Load the classified CSV file
df = pd.read_csv('classified_output.csv')

# Get the counts of each classification (easy, medium, hard)
classification_counts = df['classification'].value_counts()

# Create a bar graph
plt.figure(figsize=(8, 6))
classification_counts.plot(kind='bar', color=['green', 'yellow', 'red'])

# Add labels and title
plt.xlabel('Classification')
plt.ylabel('Number of Sentences')
plt.title('Sentence Classification Based on Word Count')
plt.xticks(rotation=0)

# Display the bar graph
plt.show()
