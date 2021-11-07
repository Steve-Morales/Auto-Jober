import tkinter as tk

# window dimensions and title
window = tk.Tk()
window.title("Auto Jober")
window.geometry("500x500")

# function for when Start button is clicked
def onclick():
    print(1) # placeholder

""""
prompt = tk.Label(text = "Name")
prompt.pack()
dropdown = tk.OptionMenu(window, value, *options)
"""
input = tk.Entry(window, width=30)
input.pack()
input.insert(0, "First name")

input = tk.Entry(window, width=30)
input.pack()
input.insert(0, "Last name")

input = tk.Entry(window, width=30)
input.pack()
input.insert(0, "Email Address")

input = tk.Entry(window, width=30)
input.pack()
input.insert(0, "Phone Number")



button = tk.Button(text="Start", command=onclick)
button.pack()

tk.mainloop()