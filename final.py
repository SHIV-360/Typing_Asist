import tkinter as tk
from tkinter import ttk  # Import ttk for Notebook widget
import pandas as pd
import random
import time
import os
import shutil
import subprocess

# Load the classified CSV file
df = pd.read_csv('classified_output.csv')

# Ensure no missing values in 'classification' or 'sentence' columns
df = df.dropna(subset=['classification', 'sentence'])

# Initialize global variables
selected_difficulty = None
selected_time = None
current_sentence = ""
timer_running = False
start_time = 0

# Track user inputs
typing_data = []

# CSV file to store user input data
CSV_FILE = "typing_data.csv"

# Create CSV file with headers if it doesn't exist
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["Given Sentence", "User Input"]).to_csv(CSV_FILE, index=False)

# Function to get a random sentence based on difficulty
def get_random_sentence(difficulty):
    filtered_df = df[df['classification'].str.lower() == difficulty.lower()]
    if filtered_df.empty:
        return "No sentences available for this difficulty."
    return random.choice(filtered_df['sentence'].tolist())

# Function to save user input before sentence resets
def save_user_input():
    global typing_data
    user_input = user_input_entry.get().strip()  # Get user input
    if current_sentence and user_input:
        typing_data.append({"Given Sentence": current_sentence, "User Input": user_input})
        pd.DataFrame(typing_data).to_csv(CSV_FILE, mode="a", header=False, index=False)  # Append to CSV
        typing_data.clear()  # Clear temporary list

# Function to display sentence and reset input field
def show_sentence():
    global current_sentence, timer_running, start_time
    if not selected_difficulty or not selected_time:
        sentence_label.config(text="Select difficulty & time first then add cursor to box and press enter to start.", fg="white")
        return

    save_user_input()  # Save the user’s input before resetting

    current_sentence = get_random_sentence(selected_difficulty)
    sentence_label.config(text=current_sentence, fg="white")
    user_input_entry.delete(0, tk.END)  # Clear input field

    if not timer_running:
        start_time = time.time()
        timer_running = True
        update_timer()

# Function to start timer when user types
def start_timer(event=None):
    global start_time, timer_running
    if selected_difficulty and selected_time and not timer_running:
        start_time = time.time()
        timer_running = True
        update_timer()

# Function to update timer every second
def update_timer():
    if timer_running:
        elapsed_time = int(time.time() - start_time)
        remaining_time = selected_time - elapsed_time
        if remaining_time > 0:
            timer_label.config(text=f"Time Remaining: {remaining_time}s")
            window.after(1000, update_timer)
        else:
            stop_timer()

# Function to stop timer
def stop_timer():
    global timer_running
    timer_running = False

    # File paths
    a_file = 'typing_data.csv'
    b_file = '21_day.csv'

    timer_label.config(text="Time's up!", fg="red")
    save_user_input()  # Save final input before stopping

    window.update()  # Force GUI to update immediately
    display_typing_metrics_popup()  # Call the updated metrics popup window
    # Append data from a.csv to b.csv
    with open(a_file, 'r') as a, open(b_file, 'a') as b:
        b.write(a.read())

    # Clear the contents of a.csv
    with open(a_file, 'w') as a:
        a.truncate(0)

# Function to display typing metrics in a separate top-level window (popup)
def display_typing_metrics_popup():
    global selected_time

    if not os.path.exists(CSV_FILE):
        return

    # Read all typing data from the CSV file
    typing_data_df = pd.read_csv(CSV_FILE)

    total_letters = 0
    correct_letters = 0

    # Calculate the total number of letters and correct letters
    for index, row in typing_data_df.iterrows():
        given_sentence = row[0]  # First column: Given Sentence
        user_input = row[1]  # Second column: User Input

        # Count total letters (excluding spaces)
        total_letters += len(given_sentence.replace(" ", ""))

        # Count correct letters
        correct_letters += sum(1 for gs, ui in zip(given_sentence.replace(" ", ""), user_input.replace(" ", "")) if gs == ui)

    # Calculate correct letters per second
    correct_letters_per_second = correct_letters / selected_time if selected_time else 0

    # Create a new window for the metrics (popup)
    metrics_popup = tk.Toplevel(window)
    metrics_popup.title("Typing Metrics")
    metrics_popup.geometry("400x250")
    metrics_popup.configure(bg="#222222")

    result_text = f"Total Character: {total_letters}\n"
    result_text += f"Correct Character : {correct_letters}\n"
    result_text += f"Correct Character Per Second: {correct_letters_per_second:.2f}"

    metrics_label = tk.Label(metrics_popup, text=result_text, font=("Comic Sans MS", 14, "bold"), fg="white", bg="#222222")
    metrics_label.pack(pady=20)

    # Close button in metrics popup
    close_button = tk.Button(metrics_popup, text="Close", font=("Comic Sans MS", 12, "bold"), bg="red", fg="white", command=metrics_popup.destroy)
    close_button.pack(pady=10)

# Function to reset the application
def reset_app():
    global selected_difficulty, selected_time, current_sentence, timer_running, start_time
    selected_difficulty = None
    selected_time = None
    current_sentence = ""
    timer_running = False
    start_time = 0

    sentence_label.config(text="", fg="white")
    user_input_entry.delete(0, tk.END)
    timer_label.config(text="")
    metrics_label.config(text="")

# Function to set difficulty
def set_difficulty(difficulty):
    global selected_difficulty
    selected_difficulty = difficulty
    show_sentence()

# Function to set selected time
def select_time(time):
    global selected_time
    selected_time = time
    timer_label.config(text=f"Time Remaining: {selected_time}s")

# Function to run the external Python file
def run_external_script():
    # Run another Python script (e.g., 'another_script.py')
    subprocess.run(["python", "try.py"])

# Create the main window
window = tk.Tk()
window.title("Typing Speed Trainer")
window.geometry("700x600")
window.configure(bg="#222222")

# Create a Notebook widget for tabs
notebook = ttk.Notebook(window)
notebook.pack(fill="both", expand=True)

# Create the first frame (Typing Trainer Tab)
typing_frame = tk.Frame(notebook, bg="#222222")
notebook.add(typing_frame, text="Typing Trainer")

# Difficulty selection
difficulty_label = tk.Label(typing_frame, text="Select Difficulty:", font=("Comic Sans MS", 13, "bold"), fg="white", bg="#222222")
difficulty_label.pack(pady=5)

button_frame = tk.Frame(typing_frame, bg="#222222")
button_frame.pack()

difficulty_levels = {"Easy": "#4CAF50", "Medium": "#FFC107", "Hard": "#E53935"}

for difficulty, color in difficulty_levels.items():
    tk.Button(button_frame, text=difficulty, font=("Comic Sans MS", 12), bg=color, fg="black",
              width=10, command=lambda d=difficulty.lower(): set_difficulty(d)).pack(side="left", padx=10, pady=5)

# Time selection
time_label = tk.Label(typing_frame, text="Select Time:", font=("Comic Sans MS", 13, "bold"), fg="white", bg="#222222")
time_label.pack(pady=5)

time_frame = tk.Frame(typing_frame, bg="#222222")
time_frame.pack()

time_options = {"10s": 10, "30s": 30, "2m": 120}

for label, value in time_options.items():
    tk.Button(time_frame, text=label, font=("Comic Sans MS", 12), bg="#2196F3", fg="black",
              width=8, command=lambda t=value: select_time(t)).pack(side="left", padx=10, pady=5)

# Sentence display, user input, timer label, and reset button
sentence_label = tk.Label(typing_frame, text="", wraplength=600, font=("Comic Sans MS", 14, "bold"), justify="center", bg="#333333", fg="white")
sentence_label.pack(pady=20, fill="both")

user_input_entry = tk.Entry(typing_frame, font=("Comic Sans MS", 12), width=60, justify="center")
user_input_entry.pack(pady=5)
user_input_entry.bind('<Return>', lambda event: show_sentence())  # Capture input on Enter

timer_label = tk.Label(typing_frame, text="", font=("Comic Sans MS", 14, "bold"), fg="white", bg="#222222")
timer_label.pack(pady=5)

metrics_label = tk.Label(typing_frame, text="", font=("Comic Sans MS", 14, "bold"), fg="white", bg="#222222")
metrics_label.pack(pady=20)

tk.Button(typing_frame, text="Reset", font=("Comic Sans MS", 12, "bold"), bg="red", fg="white", command=reset_app).pack(pady=10)

# 21 Day Analysis button to run external script
tk.Button(typing_frame, text="Run 21 Day Analysis", font=("Comic Sans MS", 12, "bold"), bg="#FF9800", fg="black", command=run_external_script).pack(pady=10)

# Create the second frame (Instructions Tab)
instructions_frame = tk.Frame(notebook, bg="#222222")
notebook.add(instructions_frame, text="Instructions")

instructions_label = tk.Label(instructions_frame, text="Steps to Use it:", font=("Comic Sans MS", 16, "bold"), fg="white", bg="#222222")
instructions_label.pack(pady=20)

instructions_text = tk.Label(instructions_frame, text="1. Select a difficulty level.\n2. Choose the time duration.\n3. Start typing the sentence as fast as possible once you feel you have done press ENTER for next sentence.\n4. View your typing speed and accuracy after time runs out.\n5. Although you can see it any time but after 21 day check your analysis.", font=("Comic Sans MS", 12), fg="white", bg="#222222")
instructions_text.pack(pady=10)

made_with_love_label = tk.Label(instructions_frame, text="Made with ❤️ by Shivang", font=("Comic Sans MS", 14, "bold"), fg="white", bg="#222222")
made_with_love_label.pack(pady=10)

window.mainloop()
