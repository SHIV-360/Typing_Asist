import tkinter as tk
import pandas as pd
import random

# Load the classified CSV file
df = pd.read_csv('classified_output.csv')

# Function to filter sentences based on selected difficulty
def get_random_sentence(difficulty):
    filtered_df = df[df['classification'] == difficulty]
    return random.choice(filtered_df['sentence'].tolist())

# Function to update the label with a random sentence based on the selected difficulty
def show_sentence(difficulty):
    sentence = get_random_sentence(difficulty)
    sentence_label.config(text=sentence, fg="white")
    global current_sentence
    current_sentence = sentence

# Function to check if the user's input matches the displayed sentence
def check_sentence(event=None):
    user_input = user_input_entry.get().strip()
    formatted_sentence = current_sentence.strip()
    
    if user_input == formatted_sentence:
        result_label.config(text="✅ Correct!", fg="#4CAF50", font=("Comic Sans MS", 14, "bold"))
    else:
        result_label.config(text="❌ Incorrect. Try again!", fg="#E53935", font=("Comic Sans MS", 14, "bold"))

# Create the main window
window = tk.Tk()
window.title("Sentence Typing Trainer")
window.geometry("550x350")
window.configure(bg="#212121")  # Dark background

# Set a modern font
font_style = ("Comic Sans MS", 12, "bold")

# Difficulty selection label
difficulty_label = tk.Label(window, text="Choose Difficulty:", font=("Comic Sans MS", 13, "bold"), fg="white", bg="#212121")
difficulty_label.pack(pady=5)

# Difficulty buttons
button_frame = tk.Frame(window, bg="#212121")
button_frame.pack()

difficulty_levels = {
    "Easy": "#4CAF50",   # Green
    "Medium": "#FFC107", # Yellow
    "Hard": "#E53935"    # Red
}

for difficulty, color in difficulty_levels.items():
    btn = tk.Button(
        button_frame, text=difficulty, font=font_style, bg=color, fg="black",
        width=10, height=1, relief="flat",
        command=lambda d=difficulty.lower(): show_sentence(d)
    )
    btn.pack(side="left", padx=10, pady=5)

# Sentence display label
sentence_label = tk.Label(window, text="", wraplength=450, font=("Comic Sans MS", 14, "bold"), 
                          justify="center", bg="#212121", fg="white")
sentence_label.pack(pady=10)

# Entry widget
user_input_entry = tk.Entry(window, font=font_style, width=50, justify="center")
user_input_entry.pack(pady=5)
user_input_entry.bind('<Return>', check_sentence)

# Check button
check_button = tk.Button(window, text="Check", command=check_sentence, font=font_style, bg="#2196F3", fg="white", 
                         width=10, height=1, relief="flat")
check_button.pack(pady=5)

# Result label
result_label = tk.Label(window, text="", font=("Comic Sans MS", 14, "bold"), bg="#212121")
result_label.pack(pady=10)

# Variable to store the current displayed sentence for comparison
current_sentence = ""

# Run the Tkinter event loop
window.mainloop()
