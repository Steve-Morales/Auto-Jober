import tkinter as tk

# window dimensions and title
window = tk.Tk()
window.title("Auto Jober")
window.geometry("500x300")

def onclick():
    # function for when Start button is clicked
    print(1) # placeholder

""""
prompt = tk.Label(text = "Name")
prompt.pack()
dropdown = tk.OptionMenu(window, value, *options)
"""
input = tk.Entry(window, width=30)
input.pack()
input.insert(0, "Enter your name")

button = tk.Button(text="Start", command=onclick)
button.pack()

tk.mainloop()