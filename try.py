import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import Label, Text, Frame
from PIL import Image, ImageTk
from collections import Counter

# Load CSV (First column = correct text, Second column = user-typed text)
df = pd.read_csv("21_day.csv", header=None)

# Dictionary to store errors
error_data = []

# Function to analyze typing errors
def analyze_errors(correct, typed):
    correct = correct.replace(" ", "")  # Remove spaces
    typed = typed.replace(" ", "")  # Remove spaces

    min_length = min(len(correct), len(typed))

    for i in range(min_length):
        if correct[i] != typed[i]:  # Substitution
            error_data.append({
                "expected": correct[i],
                "typed": typed[i],
                "position": i,
                "error_type": "substitution",
                "details": f"Substituted '{correct[i]}' with '{typed[i]}' at position {i+1}"
            })

    for i in range(min_length, len(correct)):  # Deletion
        error_data.append({
            "expected": correct[i],
            "typed": "_MISSING_",
            "position": i,
            "error_type": "deletion",
            "details": f"Deleted '{correct[i]}' at position {i+1}"
        })

    for i in range(min_length, len(typed)):  # Insertion
        error_data.append({
            "expected": "_EXTRA_",
            "typed": typed[i],
            "position": i,
            "error_type": "insertion",
            "details": f"Inserted '{typed[i]}' at position {i+1}"
        })

# Process each row
for _, row in df.iterrows():
    analyze_errors(row[0], row[1])

# Convert to DataFrame
error_df = pd.DataFrame(error_data)

# Error Type Frequency
error_type_counts = error_df['error_type'].value_counts()

# Get top 5 most frequent substitutions
substitution_errors = [error for error in error_data if error["error_type"] == "substitution"]
substitution_pairs = [(error['expected'], error['typed']) for error in substitution_errors]
substitution_count = Counter(substitution_pairs)
top_5_substitutions = substitution_count.most_common(5)

# Plot and save error type frequency graph
plt.figure(figsize=(8, 6))
error_type_counts.plot(kind='bar', color=['lightblue', 'lightgreen', 'salmon'])
plt.title('Error Type Frequency')
plt.xlabel('Error Type')
plt.ylabel('Frequency')
plt.xticks(rotation=0)
plt.savefig("error_type.png")  
plt.close()

# Error Location Analysis
total_chars = len(error_df)
beginning_threshold = total_chars // 3
middle_threshold = 2 * total_chars // 3

beginning_errors = error_df[error_df['position'] < beginning_threshold]
middle_errors = error_df[(error_df['position'] >= beginning_threshold) & (error_df['position'] < middle_threshold)]
end_errors = error_df[error_df['position'] >= middle_threshold]

# Plot and save error location graph
location_counts = [len(beginning_errors), len(middle_errors), len(end_errors)]
plt.figure(figsize=(8, 6))
plt.bar(['Beginning', 'Middle', 'End'], location_counts, color='lightcoral')
plt.title('Error Location Frequency')
plt.xlabel('Text Location')
plt.ylabel('Error Frequency')
plt.savefig("error_location.png")  
plt.close()

# Prepare detailed error explanation for top 5 substitutions
detailed_errors = "\nTop 5 Most Frequent Substitutions:\n"
for pair, count in top_5_substitutions:
    detailed_errors += f"Substituted '{pair[0]}' with '{pair[1]}' {count} times\n"

# Prepare text summary
summary_text = "Typing Analysis Report\n\n"
summary_text += "Most Frequent Error Types:\n"
for error_type, count in error_type_counts.items():
    summary_text += f"- {error_type.capitalize()} Errors: {count}\n"

summary_text += "\nError Analysis by Position:\n"
summary_text += detailed_errors  # Add the detailed errors to the summary text

if len(beginning_errors) > len(middle_errors) and len(beginning_errors) > len(end_errors):
    summary_text += "\nYou make most errors at the beginning of the text.\nSuggestion: Focus on accuracy in the first few characters.\n"
elif len(middle_errors) > len(beginning_errors) and len(middle_errors) > len(end_errors):
    summary_text += "\nYou make most errors in the middle of the text.\nSuggestion: Avoid rushing through the middle.\n"
else:
    summary_text += "\nYou make most errors towards the end of the text.\nSuggestion: Slow down towards the end.\n"

# UI Setup
root = tk.Tk()
root.title("Typing Error Analysis")
root.configure(bg="black")

# Load and resize images
img_size = (500, 350)  

error_type_img = Image.open("error_type.png").resize(img_size, Image.Resampling.LANCZOS)
error_type_photo = ImageTk.PhotoImage(error_type_img)

error_location_img = Image.open("error_location.png").resize(img_size, Image.Resampling.LANCZOS)
error_location_photo = ImageTk.PhotoImage(error_location_img)

# Display heading
heading = Label(root, text="Typing Error Analysis", font=("Comic Sans MS", 22, "bold"), fg="white", bg="black")
heading.pack(pady=10)

# Frame for images (side by side)
image_frame = Frame(root, bg="black")
image_frame.pack(pady=10)

# Display images side by side
error_type_label = Label(image_frame, image=error_type_photo, bg="black")
error_type_label.grid(row=0, column=0, padx=10)

error_location_label = Label(image_frame, image=error_location_photo, bg="black")
error_location_label.grid(row=0, column=1, padx=10)

# Display text summary
text_box = Text(root, font=("Comic Sans MS", 12), fg="white", bg="black", wrap="word", height=10, width=80)
text_box.insert("1.0", summary_text)
text_box.config(state="disabled")  
text_box.pack(pady=10)

# Run UI
root.mainloop()
