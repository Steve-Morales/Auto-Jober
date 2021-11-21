from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
#from selenium.webdriver.support import select
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time
import auto_jober_gui

# Application Global Variables
request_flag = False #determines if we need to request information from user
request_send = "Null" #type of information we need from user
request_recieve = "Null" #recieved from request
def hasRequest():
    return request_flag

def UpdateRequestVariables(false_flag, null_value, gift):
    global request_flag, request_send, request_recieve
    request_flag = false_flag
    request_send = null_value
    request_recieve = gift

def Request():
    global request_flag, request_send, request_recieve
    request_send = "Need User to Type" #type of information we need from user
    request_recieve = "Null" #recieved from request
    request_flag = True #determines if we need to request information from user
    auto_jober_gui.EvaluateRequest()

def DoSomethingToRequest():
    print("Going to Request Something")
    Request()
    print("Have requested, did it communicate first?")
    
#this is used for debugging purposes
def PrintRequestVariables():
    print("Flag: ", request_flag, "\tValue: ", request_send, "\tReturned: ", request_recieve)


# Webscraping Global Variables 
waitTime = 2                        # wait time to perform next task
username = ""        # user's username/email to login into website
password = ""         # user's password to login into website 
jobKeyword = "Software Engineer"    # keyword for related jobs

# Driver -- Global Variable -- NOT TO BE REASSIGNED
driver = webdriver.Firefox()

# Determines if the current 'form' being looked at has a 'Next' button 
# @return True (exists) or False (does not exist)
def hasNext():
    return len(driver.find_elements_by_xpath('//button[normalize-space()="Next"]')) == 1

# Clicks on a 'Next' button if one exists
def clickNext():
    driver.find_element_by_xpath('//button[normalize-space()="Next"]').click()

#go the website with set keyowrds and filters 
##### GENERALIZE KEYWORDS
def GoToWebsite():
    driver.get("https://www.linkedin.com/jobs/search/?f_AL=true&geoId=103644278&keywords=software%20engineer&location=United%20States")
    driver.find_element_by_xpath("/html/body/div[1]/header/nav/div/a[2]").click()#sign in button

#LOGIN
def LogIn():
    driver.find_element_by_xpath("//*[@id='username']").send_keys(username)
    driver.find_element_by_xpath("//*[@id='password']").send_keys(password)
    driver.find_element_by_xpath("/html/body/div/main/div[2]/div[1]/form/div[3]/button").click()

#GET JOB LIST
def GetJobList():
    html_list = driver.find_element_by_class_name("jobs-search-results");#parent-all the jobs
    return html_list.find_elements_by_tag_name("li")#children-individual jobs

# GET FORM ITEMS (WEB OBJECT CONTAING QUESTIONS AND ANSWERS)
def GetFormItems():
    #Get Form
    form_div = driver.find_element_by_xpath('//*[@id="artdeco-modal-outlet"]')#divider containing form
    apply_form = form_div.find_element_by_tag_name("form")#the form itself
    form_groups = apply_form.find_elements_by_class_name("jobs-easy-apply-form-section__grouping")#items/divders in form 
    items = []
    for group in form_groups:
        main_items = group.find_elements_by_class_name("fb-form-element.mt4.jobs-easy-apply-form-element")#multiple items
        for item in main_items:
            items.append(item)
    return items

# GET QUESTIONS FROM FORM
def GetAllQuestions(form_items):
    questions = []
    for item in form_items:#Questions
        temp = item.find_elements_by_tag_name("span")#Note: use of 'elements' to get every 'span' tag object
        for q in temp:#since we searching for 1 or more 'span' tag object, this creates a list we need to unpack
            #print(q.text)
            if q.text != "Required":
                questions.append(q.text)
    return questions

# Caveat: if there are muliple questions in a particular 'form_item' you can't guarentee you will get all answers 
def GetAllAnswers(form_items):
    answers = []
    for item in form_items:#question Answers
        try:
            temp = item.find_element_by_tag_name("input")
            #print(temp.text)
            answers.append(temp)
        except NoSuchElementException:
            print("There is no 'input' tag")
        
        try:
            #print("attempting to read drop down\n")
            temp = item.find_element_by_class_name("fb-dropdown")
            options = temp.find_elements_by_tag_name("option")
            #for a in options:
            #    print(a.text)
            if options[0].text == "Select an option":
                options.remove(options[0])
            answers.append(options)
        except NoSuchElementException:
            print("There is no dropdown")
        
        try: 
            temp = item.find_element_by_class_name("fb-radio-buttons")
            options = temp.find_elements_by_class_name("fb-radio display-flex")
            #for a in options:
            #    print(a.text)
            answers.append(options)
        except NoSuchElementException:
            print("There is no radio buttons")
    return answers

# FOR DEBUGGING
def PrintQuestions(questions):
    for q in questions:
        print(q.text)
def PrintAnswers(answers):
    for a in answers:
        try:
            for element in a:
                print(element.text)
        except:
            print(a.text)

question_dictionary = []
answer_dictionary = []

def InputGetAnswer(question):
    return auto_jober_gui.GetUserInput(question)

# web_element is the selected element that is the input box
def InputSetAnswer(answer, web_element):
    web_element.send_keys(answer)

def DropdownGetAnswer(question, options):
    choices = []
    for option in options:
        choices.append(option.text)
    return auto_jober_gui.GetUserChoice(question, choices)

# select_web_element is the element that has selectable input(s) (dropdown)
def DropdownSetAnswer(answer, select_web_element):
    sel = Select(select_web_element)
    sel.select_by_visible_text(answer)
    select_web_element.send_keys(Keys.RETURN)
    #Select(select_web_element).select_by_index(1)

def GetQuestion(form_item):
    questions = form_item.find_elements_by_tag_name("span")
    for q in questions:
        if q.text != 'Required':
            return q.text
    return q.text

# asks and inputs answer from user
def UpdateInput(item):
    try:
        temp = item.find_element_by_tag_name("input")
        if temp.text == "":
            answer = InputGetAnswer(GetQuestion(item))
            InputSetAnswer(answer, temp)#get answer from user, then type answer
        return
    except NoSuchElementException:
        pass
        #print("There is no 'input' tag")#for debugging

    try:#remember to remove the "Select an option" option for parameter
        temp = item.find_element_by_class_name("fb-dropdown").find_element_by_tag_name("select")
        val = Select(temp).first_selected_option.get_attribute('value')
        choices = Select(temp).options
        choices.pop(0)
        #if val == "Select an option":
        answer = DropdownGetAnswer(GetQuestion(item), choices)#get answer from user, then select answer
        DropdownSetAnswer(answer, temp)
        return
    except NoSuchElementException:
        pass
        #print("There is no dropdown")#for debugging

    try:#assume that no ansawer is choosen
        temp = item.find_element_by_class_name("fb-radio-buttons")
        ClickAnswer(GetAnswer())#get answer from user, then click answer/radio button
        return
    except NoSuchElementException:
        pass
        #print("There is no radio buttons")#for debugging

#APPLY THROUGH EACH JOB
def ApplyToJobs(): #for the moment we don't want this to run -- eventually we turn this into a function
    i=1
    GoToWebsite()
    LogIn()
    jobList = GetJobList()
    for job in jobList:
        print(i)
        job.click()
        driver.find_element_by_class_name("jobs-apply-button").click()
        
        form_items = GetFormItems()
        #questions = GetAllQuestions(form_items)
        #answers = GetAllAnswers(form_items)

        # checks if answers are empty for any question and then fills in the answer from either database/dictionary
        # or asks user for an answer and will remember it. 
        for item in form_items:
            UpdateInput(item)
                
        
        time.sleep(1000)
        
        while (hasNext()):
            clickNext()
        time.sleep(waitTime)
        #driver.find_element_by_xpath("//div[@class='jobs-apply-button--top-card']/button[@class='jobs-apply-button artdeco-button']").click()
        print(job.text + "\n")
        driver.execute_script("window.scrollTo(0, 100)")
        i += 1
#from auto_jober_gui import * 
#Notes:
#       *questions and answers are collected from top to bottom, left to right
#        lists that directly scrape answers or questions are in that order (i.e question[3] corresponds to answer[3]) 