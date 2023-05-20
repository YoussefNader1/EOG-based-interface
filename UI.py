import tkinter as tk

# Create the main window
root = tk.Tk()

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Define the size of the main window
window_width = 500
window_height = 400

# Calculate the x and y coordinates for the main window to center it
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the position and size of the main window to center it
root.geometry(f"{window_width}x{window_height}+{x}+{y}")


# Define a function to open the second window
def open_window():
    # Hide the root window
    root.withdraw()

    # Create the second window
    second_window = tk.Toplevel(root)
    second_window.title("Menu")
    second_window.geometry("400x400")  # Set the size of the window
    second_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Define some subdued colors for the buttons
    red = "#FF0000"
    green = "#a6df9a"
    blue = "#1E90FF"
    yellow = "#ffea8b"
    purple = "#d18bff"

    # Create the four buttons in the second window
    top = tk.Button(second_window, text="Top", width=10, height=2, fg="white", bg=blue)
    left = tk.Button(second_window, text="Left", width=10, height=2, fg="white", bg=blue)
    down = tk.Button(second_window, text="Down", width=10, height=2, fg="white", bg=blue)
    right = tk.Button(second_window, text="Right", width=10, height=2, fg="white", bg=blue)
    blink = tk.Button(second_window, text="Blink", width=10, height=2, fg="white", bg=blue)

    # Position the buttons in the second window using the grid geometry manager
    top.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    left.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    down.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
    right.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
    blink.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

    # Set the grid weights to center the buttons within the window
    second_window.columnconfigure(0, weight=1)
    second_window.columnconfigure(1, weight=1)
    second_window.columnconfigure(2, weight=1)
    second_window.rowconfigure(0, weight=1)
    second_window.rowconfigure(1, weight=1)
    second_window.rowconfigure(2, weight=1)

    def close_window():
        root.destroy()
        second_window.destroy()

    # Bind the closing event of the second window to the close_window function
    second_window.protocol("WM_DELETE_WINDOW", close_window)

    def flash_button(button):
        # Toggle the background color of the button
        if button["bg"] == red:
            button["bg"] = blue
        else:
            button["bg"] = red
        # Schedule the next function call after 500 milliseconds
        second_window.after(200, flash_button, button)

    # Start the button flashing
    output = 'blink'
    if output == 'top':
        flash_button(top)
    elif output == 'left':
        flash_button(left)
    elif output == 'down':
        flash_button(down)
    elif output == 'right':
        flash_button(right)
    elif output == 'blink':
        flash_button(blink)


# Create the button in the main window
button = tk.Button(root, text="Open menu", command=open_window, width=10, height=2, fg="white", bg="purple")

button.grid(row=0, column=0, padx=20, pady=20, sticky="")

# Set the grid weights to center the button within the window
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Set the title of the main window
root.title("Main window")

# Run the main loop
root.mainloop()
