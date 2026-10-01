import tkinter as tk
from tkinter import ttk
import threading
import time
import pyautogui
import json
import os

CONFIG_FILE = "config.json"

# Load the configuration from a JSON file
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error reading config file.")
            
    return {"key": "", "interval": 1.0}

# Save the configuration to a JSON file
def save_config(key, interval):
    config = {"key": key, "interval": interval}
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
    except Exception as e:
        print(f"Error saving config file: {e}")

# Save and cleanly close
def save_and_quit():
    save_config(key_press_entry.get(), interval_value.get())
    root.destroy()
    
# Main application window
root = tk.Tk()
root.title("Auto Key Presser")
root.geometry("350x200")

root.protocol("WM_DELETE_WINDOW", save_and_quit)

# For columns and rows 0 to 5
for col in range(6):
    root.columnconfigure(col, weight=2)
for row in range(6):
    root.rowconfigure(row, weight=1)
    
saved_config = load_config()

# Validation function to ensure only floats are typed
def validate_float(new_value):
    if new_value == "":
        return True # Allow deleting the text to type a new number
    try:
        float(new_value)
        return True
    except ValueError:
        return False # Reject the keystroke if it's not a valid float

# Register the validation command with tkinter
vcmd = (root.register(validate_float), '%P')

# Function to listen for the next key press
def start_listening():
    set_key_button.config(text="Listening...", state="disabled")
    # Listen for the very next key press anywhere on the window
    root.bind('<Key>', capture_key)

def capture_key(event):
    key_name = event.keysym.lower()
    
    # Map tkinter's 'return' key to pyautogui's 'enter' key
    if key_name == 'return':
        key_name = 'enter'

    # Temporarily enable the entry to change its text
    key_press_entry.config(state="normal")
    key_press_entry.delete(0, tk.END)
    key_press_entry.insert(0, key_name)
    
    # Lock it back to readonly
    key_press_entry.config(state="readonly")
    
    # Reset button and stop listening for keys
    set_key_button.config(text="Set Key", state="normal")
    root.unbind('<Key>')

# Create a frame to hold the widgets
key_press_label = ttk.Label(root, text="Key to Press:")
key_press_label.grid(column=0, row=1, sticky="e", padx=5)

# Readonly entry to display the captured key
key_press_entry = ttk.Entry(root)
key_press_entry.insert(0, saved_config.get("key", ""))  # Default key value
key_press_entry.config(state="readonly")
key_press_entry.grid(column=1, row=1, sticky="ew", padx=5)

# Button to set the key
set_key_button = ttk.Button(root, text="Set Key", command=start_listening)
set_key_button.grid(column=2, row=1, sticky="w", padx=5)

interval_label = ttk.Label(root, text="Interval (s):")
interval_label.grid(column=0, row=2, sticky="e", padx=5)

# Spinbox for interval input with validation
interval_value = ttk.Spinbox(
    root, 
    from_=0.1, 
    to=9999.0, 
    increment=0.1, 
    validate="key", 
    validatecommand=vcmd
)
interval_value.insert(0, saved_config.get("interval", "1.0"))  # Default interval value
interval_value.grid(column=1, row=2, sticky="ew", padx=5)

is_started = False

def auto_key_presser(key, interval):
    global is_started
    
    while is_started:
        try:
            pyautogui.press(key)
        except Exception as e:
            # Failsafe: stop if PyAutoGUI doesn't recognize the captured key
            print(f"Error pressing key: {e}")
            is_started = False
            start_stop_button.config(text="Start")
            break
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
start_stop_button.grid(column=0, row=5, columnspan=2, sticky="e", padx=5, pady=5)

quit_button = ttk.Button(root, text="Quit", command=save_and_quit)
quit_button.grid(column=5, row=5, sticky="e", padx=5, pady=5)

root.mainloop()