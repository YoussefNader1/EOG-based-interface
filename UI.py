import tkinter as tk

# Create the main window
root = tk.Tk()


# Define a function to open the second window
def open_window():
    # Create the second window
    second_window = tk.Toplevel(root)
    second_window.title("Menu")
    second_window.geometry("400x400")  # Set the size of the window

    # Define some subdued colors for the buttons
    red = "#ff8b8b"
    green = "#a6df9a"
    blue = "#8b8bff"
    yellow = "#ffea8b"
    purple = "#d18bff"

    # Create the four buttons in the second window
    button1 = tk.Button(second_window, text="Sleep", width=10, height=2, fg="white", bg=red)
    button2 = tk.Button(second_window, text="Eat", width=10, height=2, fg="white", bg=green)
    button3 = tk.Button(second_window, text="Drink water", width=10, height=2, fg="white", bg=blue)
    button4 = tk.Button(second_window, text="Go to bathroom", width=10, height=2, fg="white", bg=yellow)
    button5 = tk.Button(second_window, text="Choice", width=10, height=2, fg="white", bg=purple)

    # Position the buttons in the second window using the grid geometry manager
    button1.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    button2.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    button3.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
    button4.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
    button5.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

    # Set the grid weights to center the buttons within the window
    second_window.columnconfigure(0, weight=1)
    second_window.columnconfigure(1, weight=1)
    second_window.columnconfigure(2, weight=1)
    second_window.rowconfigure(0, weight=1)
    second_window.rowconfigure(1, weight=1)
    second_window.rowconfigure(2, weight=1)


# # Load the image file
# bg_image = tk.PhotoImage(file="background.png")
#
# # Set the background image of the main window
# root.configure(bg=bg_image)

# Create the button in the main window
button = tk.Button(root, text="Open menu", command=open_window, width=10, height=2, fg="white", bg="purple")

button.grid(row=0, column=0, padx=20, pady=20, sticky="")

# Set the grid weights to center the button within the window
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Set the size of the main window
root.geometry("500x400")

root.title("Main window")

# Run the main loop
root.mainloop()
