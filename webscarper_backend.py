from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
import time

waitTime = 2

username = ""
password = ""
jobKeyword = "Software Engineer"

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
driver.get("https://www.linkedin.com/jobs/search/?f_AL=true&geoId=103644278&keywords=software%20engineer&location=United%20States")
driver.find_element_by_xpath("/html/body/div[1]/header/nav/div/a[2]").click()#sign in button

#LOGIN
driver.find_element_by_xpath("//*[@id='username']").send_keys(username)
driver.find_element_by_xpath("//*[@id='password']").send_keys(password)
driver.find_element_by_xpath("/html/body/div/main/div[2]/div[1]/form/div[3]/button").click()

#GET JOB LIST
html_list = driver.find_element_by_class_name("jobs-search-results");#parent-all the jobs
jobList = html_list.find_elements_by_tag_name("li")#children-individual jobs

def GetFormItems():
    #Get Form
    form_div = driver.find_element_by_xpath('//*[@id="artdeco-modal-outlet"]')#divider containing form
    apply_form = form_div.find_element_by_tag_name("form")#the form itself
    return apply_form.find_elements_by_class_name("jobs-easy-apply-form-section__grouping")#items/divders in form 

def GetQuestions(form_items):
    questions = []
    for item in form_items:#Questions
        temp = item.find_elements_by_tag_name("span")#Note: use of 'elements' to get every 'span' tag object
        for q in temp:#since we searching for 1 or more 'span' tag object, this creates a list we need to unpack
            #print(q.text)
            if q.text != "Required":
                questions.append(q)
    return questions

# Caveat: if there are muliple questions in a particular 'form_item' you can't guarentee you will get all answers 
def GetAnswers(form_items):
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

#APPLY THROUGH EACH JOB
i = 1
for job in jobList:
    print(i)
    job.click()
    driver.find_element_by_class_name("jobs-apply-button").click()
    
    form_items = GetFormItems()
    questions = GetQuestions(form_items)
    answers = GetAnswers(form_items)
    
    
    temp = Select(form_items[0].find_element_by_class_name("fb-dropdown").find_element_by_tag_name("select"))
    val = temp.first_selected_option.get_attribute('value')
    print(val)

    # checks if answers are empty for any question and then fills in the answer from either database/dictionary
    # or asks user for an answer and will remember it. 
    # Caveat: if there are muliple questions in a particular 'form_item' you can't guarentee you will get all answers 
    for item in form_items:
        try:
            temp = item.find_element_by_tag_name("input")
            if temp == "":
                TypeAnswer(GetAnswer());#get answer from user, then type answer
        except NoSuchElementException:
            print("There is no 'input' tag")
        
        try:
            temp = item.find_element_by_class_name("fb-dropdown").find_element_by_tag_name("select")
            val = Select(temp).first_selected_option.get_attribute('value')
            if val == "Select an option":
                SelectAnswer(GetAnswer())#get answer from user, then select answer
        except NoSuchElementException:
            print("There is no dropdown")
        
        try:#assume that no ansawer is choosen
            temp = item.find_element_by_class_name("fb-radio-buttons")
            ClickAnswer(GetAnswer())#get answer from user, then click answer/radio button
        except NoSuchElementException:
            print("There is no radio buttons")
    
    time.sleep(1000)
    
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