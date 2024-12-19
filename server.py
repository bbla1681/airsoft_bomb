from flask import Flask, request
import threading
import tkinter as tk
import time

app = Flask(__name__)

root = None  # Global variable for the Tkinter root window
def initialize_tkinter_window():
    global root
    root = tk.Tk()
    root.title("Bomb Overview")
    root.geometry("300x250")
    root.configure(bg="red")

    label = tk.Label(root, text="DEACTIVATED", font=("Arial", 24), bg="red", fg="white")
    label.pack(pady=20)

def activate_tkinter_window():
    global root
    if root:
        for widget in root.winfo_children():
            widget.destroy()
        root.configure(bg="green")

        label = tk.Label(root, text="ACTIVATED", font=("Arial", 24), bg="green", fg="white")
        label.pack(pady=20)

        global timer_label
        timer_label = tk.Label(root, text="03:00", font=("Arial", 20), bg="green", fg="white")
        timer_label.pack(pady=10)

        def countdown():
            time_left = 180  # 3 minutes in seconds
            while time_left > 0:
                minutes, seconds = divmod(time_left, 60)
                timer_label.config(text=f"{minutes:02}:{seconds:02}")
                time.sleep(1)
                time_left -= 1
            timer_label.config(text="00:00")

        threading.Thread(target=countdown, daemon=True).start()

        root.update()

def deactivate_tkinter_window():
    global root
    if root:
        for widget in root.winfo_children():
            widget.destroy()
        root.configure(bg="red")

        label = tk.Label(root, text="DEACTIVATED", font=("Arial", 24), bg="red", fg="white")
        label.pack(pady=20)

        root.update()

@app.route("/activate", methods=["GET"])
def activate():
    threading.Thread(target=activate_tkinter_window, daemon=True).start()
    return {"status": "Tkinter window activated"}, 200

@app.route("/deactivate", methods=["GET"])
def deactivate():
    threading.Thread(target=deactivate_tkinter_window, daemon=True).start()
    return {"status": "Tkinter window deactivated"}, 200

def run_flask():
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    initialize_tkinter_window()
    threading.Thread(target=run_flask, daemon=True).start()
    root.mainloop()
