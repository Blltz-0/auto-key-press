import tkinter as tk
from tkinter import ttk
import threading
import time
import pyautogui

# Main application window
root = tk.Tk()
root.title("Auto Key Presser")
root.geometry("300x200")

# For columns and rows 0 to 5
for col in range(6):
    root.columnconfigure(col, weight=1)
for row in range(6):
    root.rowconfigure(row, weight=1)

# Create a frame to hold the widgets

key_press_label = ttk.Label(root, text="Key to Press:")
key_press_label.grid(column=0, row=1, sticky="e")
key_press_entry = ttk.Entry(root)
key_press_entry.grid(column=1, row=1, sticky="ew")

interval_label = ttk.Label(root, text="Interval (seconds):")
interval_label.grid(column=0, row=2, sticky="e")
interval_value = ttk.Entry(root)
interval_value.insert(0, "1.0")  # Default interval value
interval_value.grid(column=1, row=2, sticky="ew")

is_started = False

def auto_key_presser(key, interval):
    global is_started
    
    while is_started:
        pyautogui.press(key)
        time.sleep(interval)
        

def toggle_start_stop():
    global is_started
    
    if not is_started:
        key = key_press_entry.get()
        try:
            interval = float(interval_value.get())
        except ValueError:
            print("Invalid interval value. Please enter a number.")
            return
        
        if not key:
            print("Please enter a key to press.")
            return
        
        is_started = True
        start_stop_button.config(text="Stop")
        # Start the auto key presser in a separate thread
        threading.Thread(target=auto_key_presser, args=(key, interval), daemon=True).start()
    else:
        is_started = False
        start_stop_button.config(text="Start")
        
start_stop_button = ttk.Button(root, text="Start", command=toggle_start_stop)
start_stop_button.grid(column=0, row=5, columnspan=4, sticky="e", padx=5, pady=5)



quit_button = ttk.Button(root, text="Quit", command=root.destroy)
quit_button.grid(column=5, row=5, sticky="e", padx=5, pady=5)


root.mainloop()