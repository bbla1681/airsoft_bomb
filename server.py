import tkinter as tk
import threading
import requests
import time

def create_tkinter_window():
    global root, timer_label

    root = tk.Tk()
    root.title("Reference Side")
    root.geometry("300x250")
    root.configure(bg="red")

    label = tk.Label(root, text="DEACTIVATED", font=("Arial", 24), bg="red", fg="white")
    label.pack(pady=20)

    timer_label = tk.Label(root, text="", font=("Arial", 20), bg="red", fg="white")
    timer_label.pack(pady=10)

    root.mainloop()

def start_timer():
    def countdown():
        global root, timer_label

        if root:
            for widget in root.winfo_children():
                widget.destroy()
            root.configure(bg="green")

            label = tk.Label(root, text="ACTIVATED", font=("Arial", 24), bg="green", fg="white")
            label.pack(pady=20)

            timer_label = tk.Label(root, text="03:00", font=("Arial", 20), bg="green", fg="white")
            timer_label.pack(pady=10)

            time_left = 180  # 3 minutes in seconds
            while time_left > 0:
                minutes, seconds = divmod(time_left, 60)
                timer_label.config(text=f"{minutes:02}:{seconds:02}")
                time.sleep(1)
                time_left -= 1
            timer_label.config(text="00:00")

    threading.Thread(target=countdown, daemon=True).start()

def deactivate():
    global root
    if root:
        for widget in root.winfo_children():
            widget.destroy()
        root.configure(bg="red")

        label = tk.Label(root, text="DEACTIVATED", font=("Arial", 24), bg="red", fg="white")
        label.pack(pady=20)

        root.update()

def listen_to_flask():
    while True:
        try:
            response = requests.get("http://localhost:5000/status").json()
            if response.get("action") == "start_timer":
                start_timer()
            elif response.get("action") == "deactivate":
                deactivate()
        except Exception as e:
            print("Error connecting to Flask backend:", e)
        time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=create_tkinter_window, daemon=True).start()
    threading.Thread(target=listen_to_flask, daemon=True).start()
