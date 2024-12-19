import tkinter as tk
import random
from tkinter import messagebox
import time
import pygame  # For audio playback

activation_mode = True  # Start in activation phase
deactivation_mode = False  # Track deactivation phase
successful_deactivation_attempts = 0  # Counter for deactivation
countdown_job = None  # To track the countdown job

# Initialize pygame mixer for audio playback
pygame.mixer.init()

def play_audio(file_path):
    """Plays an audio file."""
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def stop_audio():
    """Stops any currently playing audio."""
    pygame.mixer.music.stop()

def generate_number():
    """Generates a random 6-digit number and displays it."""
    global random_number
    random_number = random.randint(100000, 999999)
    number_label.config(text=random_number)
    try:
        entry.delete(0, tk.END)  # Clear the text box
    except:
        pass
    stop_audio()  # Stop typing audio when number changes
    if activation_mode or deactivation_mode:
        root.after(5000, generate_number)  # Regenerate number every 5 seconds in either phase

def check_number():
    """Checks if the user-inputted number matches the generated number."""
    global activation_mode, deactivation_mode, successful_deactivation_attempts

    user_input = entry.get()
    if user_input == str(random_number):
        if activation_mode:
            messagebox.showinfo("Success", "BOMB HAS BEEN ARMED.")
            activation_mode = False
            deactivation_mode = True
            start_deactivation_timer()
        else:
            successful_deactivation_attempts += 1
            if successful_deactivation_attempts == 2:
                show_restart_screen()
            else:
                messagebox.showinfo(
                    "Success",
                    f"COMPLETED DEACTIVATION SEQUENCE STAGE {successful_deactivation_attempts}. {2 - successful_deactivation_attempts} STAGE LEFT.",
                )
    else:
        messagebox.showerror("Error", "Incorrect. Try again.")

def start_deactivation_timer():
    """Starts a 3-minute timer for the deactivation phase."""
    countdown_label.config(text="3:00")
    countdown(180)

def countdown(time_left):
    """Counts down the timer and updates the label."""
    global countdown_job, deactivation_mode, activation_mode
    if time_left > 0:
        minutes, seconds = divmod(time_left, 60)
        countdown_label.config(text=f"{minutes}:{seconds:02}", font=("Arial", 24))  # Larger font size for timer
        countdown_job = root.after(1000, countdown, time_left - 1)
    else:
        countdown_label.pack_forget()  # Remove the clock from the screen
        if deactivation_mode:
            messagebox.showinfo("Time Up", "BOOOOOOOOOOOOOM.")
            deactivation_mode = False
            activation_mode = True
            generate_number()

def show_restart_screen():
    """Displays a screen asking the user to restart."""
    global countdown_job, deactivation_mode

    # Cancel any pending countdown jobs
    if countdown_job:
        root.after_cancel(countdown_job)
        countdown_job = None

    deactivation_mode = False  # Ensure deactivation mode is reset

    for widget in root.winfo_children():
        widget.destroy()

    restart_label = tk.Label(root, text="Deactivation completed! Restart?", font=("Arial", 14))
    restart_label.pack(pady=20)

    restart_button = tk.Button(root, text="Restart", command=restart_game)
    restart_button.pack(pady=10)

def restart_game():
    """Restarts the game by resetting to the activation phase."""
    global activation_mode, successful_deactivation_attempts
    activation_mode = True
    successful_deactivation_attempts = 0
    for widget in root.winfo_children():
        widget.destroy()

    setup_game()

def setup_game():
    """Sets up the game UI."""
    global number_label, entry, countdown_label

    number_label = tk.Label(root, text="Generating number...", font=("Arial", 12))
    number_label.pack(pady=10)

    generate_number()

    entry = tk.Entry(root)
    entry.pack(pady=5)
    entry.bind("<Return>", lambda event: check_number())
    entry.focus_set()  # Automatically focus on the text box

    countdown_label = tk.Label(root, text="", font=("Arial", 24))  # Larger font size for timer
    countdown_label.pack(pady=5)

# Initialize the main window
root = tk.Tk()
root.title("Bomb")
root.geometry("300x250")

setup_game()

# Run the application
root.mainloop()
