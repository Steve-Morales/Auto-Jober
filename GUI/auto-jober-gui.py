import tkinter as tk
from tkinter import filedialog

# window dimensions and title
window = tk.Tk()
window.title("Auto Jober")
window.geometry("500x300")

# function for when Start button is clicked (backend starts running)
def onclick():
    print(resume) #placeholder

# function for asking user to upload resume/file
def uploadResume():
    resume = filedialog.askopenfilename()
    print('Selected:', resume)

""""
prompt = tk.Label(text = "Name")
prompt.pack()
dropdown = tk.OptionMenu(window, value, *options)
"""

firstName = tk.Entry(window, width=30)
firstName.pack()
firstName.insert(0, "First name")

lastName = tk.Entry(window, width=30)
lastName.pack()
lastName.insert(0, "Last name")

email = tk.Entry(window, width=30)
email.pack()
email.insert(0, "Email Address")

phoneNum = tk.Entry(window, width=30)
phoneNum.pack()
phoneNum.insert(0, "Phone Number")

jobTitle = tk.Entry(window, width=30)
jobTitle.pack()
jobTitle.insert(0, "Desired Job Title")

resume = 0
button = tk.Button(text="Upload Resume", command=uploadResume)
button.pack()

button = tk.Button(text="Start", command=onclick)
button.pack()

tk.mainloop()