import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from mutagen.mp3 import MP3

# Define constants for the lengths of the discs
MINIDISC_74_LENGTH = 74 * 60  # 74 minutes in seconds
MINIDISC_80_LENGTH = 80 * 60  # 80 minutes in seconds


# Function to calculate total duration of MP3 files in a folder
def calculate_total_duration(folder):
    total_duration = 0
    mp3_files = [f for f in os.listdir(folder) if f.endswith('.mp3')]

    if not mp3_files:
        messagebox.showerror("Error", "No MP3 files found in the selected folder.")
        return None

    for file in mp3_files:
        try:
            file_path = os.path.join(folder, file)
            audio = MP3(file_path)
            total_duration += audio.info.length
        except Exception as e:
            print(f"Error processing file {file}: {e}")

    return total_duration


# Function to calculate the percentage of a disc used by the total runtime
def calculate_disc_percentage(total_duration, disc_length):
    return (total_duration / disc_length) * 100


# Function to format the duration from seconds to mm:ss
def format_duration(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"


# Function to update the progress bars
def update_progress_bars(percent_74, percent_80):
    # Update 74-minute disc progress bar
    progress_bar_74['value'] = percent_74
    progress_label_74.config(text=f"74-minute disc usage: {percent_74:.2f}%")

    # Update 80-minute disc progress bar
    progress_bar_80['value'] = percent_80
    progress_label_80.config(text=f"80-minute disc usage: {percent_80:.2f}%")


# Function to calculate duration when a folder is selected
def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)
        status_label.config(text="Status: Calculating...")

        # Calculate the total duration of all MP3 files in the folder
        total_duration = calculate_total_duration(folder_selected)

        if total_duration is not None:
            formatted_duration = format_duration(total_duration)

            # Calculate the percentage of 74-minute and 80-minute discs used
            percent_74_used = calculate_disc_percentage(total_duration, MINIDISC_74_LENGTH)
            percent_80_used = calculate_disc_percentage(total_duration, MINIDISC_80_LENGTH)

            # Update the result labels with the total duration
            result_label.config(text=f"Total Duration: {formatted_duration}")

            # Update the progress bars
            update_progress_bars(percent_74_used, percent_80_used)

            status_label.config(text="Status: Calculation complete")
        else:
            result_label.config(text="Total Duration: 00:00")
            status_label.config(text="Status: Failed to calculate duration")


# Set up the GUI
root = tk.Tk()
root.title("MP3 Duration Calculator")
root.geometry("400x400")

# Folder selection label and textbox
folder_label = tk.Label(root, text="Select a folder:")
folder_label.pack(pady=10)

folder_path = tk.StringVar()
folder_entry = tk.Entry(root, textvariable=folder_path, width=50)
folder_entry.pack(pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.pack(pady=5)

# Result and status labels
result_label = tk.Label(root, text="Total Duration: 00:00")
result_label.pack(pady=5)

status_label = tk.Label(root, text="Status: Waiting for input...")
status_label.pack(pady=5)

# Progress bar and label for 74-minute disc usage
progress_label_74 = tk.Label(root, text="74-minute disc usage: 0.00%")
progress_label_74.pack(pady=5)

progress_bar_74 = ttk.Progressbar(root, length=300, mode='determinate')
progress_bar_74.pack(pady=5)

# Progress bar and label for 80-minute disc usage
progress_label_80 = tk.Label(root, text="80-minute disc usage: 0.00%")
progress_label_80.pack(pady=5)

progress_bar_80 = ttk.Progressbar(root, length=300, mode='determinate')
progress_bar_80.pack(pady=5)

# Start the GUI loop
root.mainloop()
