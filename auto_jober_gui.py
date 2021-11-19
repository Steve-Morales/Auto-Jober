import tkinter as tk
from tkinter import filedialog

#link backend
#import sys
#sys.path.append('/Auto-Jober/webscraper_backend.py')
#from webscraper_backend import IsBackendLinked
#import webscraper_backend as backend
#from mediator import *
import webscraper_backend
# window dimensions and title
window = tk.Tk()
window.title("Auto Jober")
window.geometry("500x300")
window.configure(bg="#0072b1")

# function for when Start button is clicked (backend starts running)
def onclick():
    # available variables: firstName, lastName, email, phoneNum, jobTitle, resume
    #print("Loging In") #placeholder
    #SiteLogIn()
    webscraper_backend.DoSomethingToRequest()

def EvaluateRequest():
    webscraper_backend.UpdateRequestVariables(False, "Null", "Request Completed")
    webscraper_backend.PrintRequestVariables()

# function for asking user to upload resume/file
# output: resume file
def uploadResume():
    global resume
    resume = filedialog.askopenfilename()

# ask for first name
firstName = tk.Entry(window, width=30)
firstName.pack()
firstName.insert(0, "First name")

# ask for last name
lastName = tk.Entry(window, width=30)
lastName.pack()
lastName.insert(0, "Last name")

# ask for email
email = tk.Entry(window, width=30)
email.pack()
email.insert(0, "Email Address")

# ask for phone number
phoneNum = tk.Entry(window, width=30)
phoneNum.pack()
phoneNum.insert(0, "Phone Number")

# ask for job title user is trying to apply for
jobTitle = tk.Entry(window, width=30)
jobTitle.pack()
jobTitle.insert(0, "Desired Job Title")

# create resume variable to allow for access outside of uploadResume function
resume = 0
resumeButton = tk.Button(text="Upload Resume", command=uploadResume)
resumeButton.pack()

# button to start back end code
startButton = tk.Button(text="Start", command=onclick)
startButton.pack()

tk.mainloop()

