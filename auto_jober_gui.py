import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import IntVar
import webscraper_backend

# import webscraper_backend

# window dimensions and title
window = tk.Tk()
window.title("Auto Jober")
window.geometry("500x300")
window.configure(bg="#0072b1")

# function for when Start button is clicked (backend starts running)
def onclick():
    # available variables: firstName, lastName, email, phoneNum, jobTitle, resume
    #
    #print("Loging In") #placeholder
    webscraper_backend.ApplyToJobs()
    #pass

########################## README ####################################
# Now that GUI is linked with the backend, and due to the circular
# dependency issue, you have to run 'webscraper_backend.py'
# 
#                  __Debugging/Testing__
# Comment out 'webscraper_backend.ApplyToJobs()' in 'def onclick()' 
# from 'auto_jober_gui.py' (i.e this file).
# Then add 'pass' right after the commented line.
# Should look like this:
# def onclick():
#       #webscraper_backend.ApplyToJobs()
#       pass
#
# To make things a bit more easier, comment out 'driver = webdriver.Firefox()'
# in 'webscraper_backend.py'
#
# To test your functions, call them before 'tk.mainloop()' with
# initilized variables that represent the parameters you want to use
# to test. (see bootom of file)
#
# Once everything works, undo the stuff you did to debug (i.e uncommenting and deleting)

########################## TODO ####################################
# will open up a dialog box prompting user to type an answer
# the parameter 'question' is the question the dialog box needs to display
# use tkinter.simpledialog.askstring(title, prompt, **kw) 
# lastly, the output of this function should be the text the user typed
def GetUserInput(question):
    print("Question: ", question)#for debugging, can be deleted

    answer = simpledialog.askstring("Input", question, parent=window)
    print("Answer: ", answer)#for debugging, can be deleted
    return answer

########################## TODO ####################################
# will open up a dialog box prompting user to select one of many choices
# the parameter 'question' is the question the dialog box needs to display
# the parameter 'choices' are the choices the user can pick from, but can only select 1
# The following may be useful: 
# https://stackoverflow.com/questions/42581016/how-do-i-display-a-dialog-that-asks-the-user-multi-choice-question-using-tkinter
# https://docs.python.org/3/library/tkinter.messagebox.html
#
# Notes: There are two routes you can take, (1) return the text of the choice the user selected
#        such as "California" (2) return the index of the selected choice, for example,
#        suppose you're given the list of choices [choice0, choice1, choice2], if the user
#        picks choice0, then return 0, where 0 is the index.
#
#        once you've tested and confirmed it works, let me know which route you've taken
def GetUserChoice(question, choices):
    if question:
        tk.Label(window, text=question).pack()
    v = IntVar()
    for i, choice in enumerate(choices):
        tk.Radiobutton(window, text=choice, variable=v, value=i).pack(anchor="w")
    tk.Button(text="Sumbit", command=window.destroy).pack()
    window.mainloop()
    if v.get() == 0: return None
    answer = choices[i]
    print("Question: ", question)#for debugging, can be deleted
    print("##Start of Choices##")#for debugging, can be deleted
    for choice in choices:#for debugging, can be deleted
        print(choice)#for debugging, can be deleted
    print("##End of Choices##")#for debugging, can be deleted
    answer = choices[0]#place holder
    print("Answer: ", answer)#for debugging, can be deleted
    return answer

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

# ask for username and password
userName = tk.Entry(window, width=30)
userName.pack()
userName.insert(0, "Linkedin Username")

passWord = tk.Entry(window, width=30)
passWord.pack()
passWord.insert(0, "Linkedin Password")

# create resume variable to allow for access outside of uploadResume function
resume = 0
resumeButton = tk.Button(text="Upload Resume", command=uploadResume)
resumeButton.pack()

# button to start back end code
startButton = tk.Button(text="Start", command=onclick)
startButton.pack()

tk.mainloop()