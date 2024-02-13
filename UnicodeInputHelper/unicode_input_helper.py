import keyboard  # for handling keyboard events
import clipboard  # for working with the clipboard
from tkinter import simpledialog, messagebox  # GUI components
from pystray import MenuItem as item, Icon  # for creating system tray
from PIL import Image  # Python Imaging Library for working with images


# Function to copy a Unicode character to the clipboard and paste it into the
# active window
def send_unicode_to_active_window(unicode_char):
    clipboard.copy(unicode_char)
    keyboard.press_and_release('backspace')  # to remove +
    keyboard.press_and_release("ctrl+v")


# Function to handle the event when the hotkey is pressed
def on_hotkey_event():
    last_value = None

    while True:
        hex_value = simpledialog.askstring(
            "Enter UTF-16 hex code", "Enter UTF-16 hex code (e.g., 1F602): ",
            initialvalue=last_value)

        if hex_value is None:
            break

        last_value = hex_value

        if hex_value:
            try:
                # Convert hex value to Unicode character
                unicode_char = chr(int(hex_value, 16))
                send_unicode_to_active_window(unicode_char)
                break
            except ValueError:
                messagebox.showinfo(
                    "Invalid hex value.",
                    "Please enter a valid UTF-16 hex code.")


# Function to handle the exit event for the system tray icon
def on_exit(icon, item):
    global keyboard
    keyboard.unhook_all()
    icon.stop()


# Function to customize waiting for a hotkey event
def custom_wait(hotkey=None, suppress=False, trigger_on_release=False):
    """
    Blocks the program execution until the given hotkey is pressed or,
    if given no parameters, stops blocking immediately.
    """
    if hotkey:
        lock = keyboard._Event()
        remove = keyboard.add_hotkey(
            hotkey, lambda: lock.set(), suppress=suppress,
            trigger_on_release=trigger_on_release)
        lock.wait()
        keyboard.remove_hotkey(remove)


# Override the wait function in the keyboard library with the custom_wait
# function
keyboard.wait = custom_wait

# Define the system tray menu with an exit option
menu = (item('Exit', on_exit),)

# Create a system tray icon with the specified menu and image
menu_icon = Icon(
    "name", Image.open("logo.png"),
    title="Unicode input helper", menu=menu)

# Run the system tray icon detached from the main program
menu_icon.run_detached()

# Add a hotkey for triggering the Unicode input event
keyboard.add_hotkey('alt+plus', on_hotkey_event)

# Wait for keyboard events indefinitely
keyboard.wait()
