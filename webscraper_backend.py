from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time
import auto_jober_gui


# Webscraping Global Variables 
waitTime = 2                        # wait time to perform next task
username = ""        # user's username/email to login into website
password = ""         # user's password to login into website 
jobKeyword = "Software Engineer"    # keyword for related jobs

# Driver -- Global Variable -- NOT TO BE REASSIGNED
driver = webdriver.Firefox()

########################## TODO ####################################
# Make sure this works
#
# Determines if the current 'form' being looked at has a 'Next' button 
# @return True (exists) or False (does not exist)
def hasNext():
    return len(driver.find_elements_by_xpath('//button[normalize-space()="Next"]')) == 1

########################## TODO ####################################
# Make sure this works
#
# Clicks on a 'Next' button if one exists
def clickNext():
    driver.find_element_by_xpath('//button[normalize-space()="Next"]').click()

#                           TODO                         #
# Since we just need something to show at the demo, this
# isn't too important.
# Need to allow any keyword(s) to be used to search for 
# jobs.
#
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

# GET FORM ITEMS (WEB OBJECT CONTAINING QUESTION AND ANSWER)
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

# GET ALL ANSWERS FROM FORM
# dropdown and radio answers are lists within 'answer' list
# having it this way maintains order 
# (i.e questions[n] has answers that pertain to answers[n] and vice versa)
# Note: getting answers from radio buttons need to be tested
def GetAllAnswers(form_items):
    answers = []
    for item in form_items:#question Answers
        try:
            temp = item.find_element_by_tag_name("input")
            #print(temp.text)
            answers.append(temp)
            continue
        except NoSuchElementException:
            pass
            #print("There is no 'input' tag")#for debugging, can be deleted
        
        try:
            #print("attempting to read drop down\n")
            temp = item.find_element_by_class_name("fb-dropdown")
            options = temp.find_elements_by_tag_name("option")
            #for a in options:
            #    print(a.text)
            if options[0].text == "Select an option":
                options.remove(options[0])
            answers.append(options)
            continue
        except NoSuchElementException:
            pass
            #print("There is no dropdown")#for debugging, can be deleted
        
        try: 
            temp = item.find_element_by_class_name("fb-radio-buttons")
            options = temp.find_elements_by_class_name("fb-radio display-flex")
            #for a in options:
            #    print(a.text)
            answers.append(options)
            continue
        except NoSuchElementException:
            pass#if it gets to this point, then there is a massive error
            #print("There is no radio buttons")#for debugging, can be deleted
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

# Using the question from the a form item, we retrieve an answer from the user
# Using the answer from the user, it selects/inputs their answer for them
def InputGetAnswer(question):
    return auto_jober_gui.GetUserInput(question)

# web_element is the input/text box
# using the answer retrieved from the user, this function types their answer
# into the textbox
def InputSetAnswer(answer, web_element):
    web_element.send_keys(answer)

# Assume that options have "acceptable-only" answers 
# (i.e "Select option" cannot be a choice for the user)
# This function retrieves and answer from the user
def DropdownGetAnswer(question, options):
    choices = []
    for option in options:
        choices.append(option.text)
    return auto_jober_gui.GetUserChoice(question, choices)

########################## TODO ####################################
# There seems to be some sort of bug where it does not choose the
# correct answer
#
# select_web_element is the element that has selectable input(s) (dropdown)
def DropdownSetAnswer(answer, select_web_element):
    sel = Select(select_web_element)
    sel.select_by_visible_text(answer)
    #select_web_element.send_keys(Keys.RETURN)
    #Select(select_web_element).select_by_index(1)

# Get's questions from the current form item
# Note: the parameter is not the list of form items,
#       but an item from the form items.
def GetQuestion(form_item):
    questions = form_item.find_elements_by_tag_name("span")
    for q in questions:
        if q.text != 'Required':
            return q.text #assumes that there are only two 'span' tag objects
    return questions.text #assumes that there was only one 'span' tag objects

########################## TODO ####################################
# -Radio buttons
# -Dropdown
#
# Retrieves answer from user and inputs answer for user
# for each item in 'form_items'
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

# Note: for any i>=0, question[i] matches with answer[i]
question_dictionary = [] #list of questions already answered
answer_dictionary = [] #list of answers for each question

########################## TODO ####################################
# Since we just need something for the demo, this does not have to be
# effecient or save any data.
# Note: this may have to come before 'UpdateInput' function
def UpdateDictionary(question, answer):
    pass

########################## TODO ####################################
# Since we just need something for the demo, this does not have to be
# effecient.
# This function should return the index of the question
# if it cannot be found, then it should return -1
def FindQuestionInDictionary(question):
    pass
# Note: I don't think we need a 'FindAnswerInDictionary' function



# APPLY THROUGH EACH JOB
# This is where we put everything together
def ApplyToJobs():
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
                
        
        time.sleep(1000)#remove this if nessesary, should be removed once everything works
        
        while (hasNext()):
            clickNext()
        time.sleep(waitTime)
        #driver.find_element_by_xpath("//div[@class='jobs-apply-button--top-card']/button[@class='jobs-apply-button artdeco-button']").click()
        print(job.text + "\n")
        driver.execute_script("window.scrollTo(0, 100)")
        i += 1
 
#Notes:
#       *questions and answers are collected from top to bottom, left to right
#        lists that directly scrape answers or questions are in that order (i.e question[3] corresponds to answer[3]) 