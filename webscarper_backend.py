from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

waitTime = 2

username = ""
password = ""
jobKeyword = "Software Engineer"

driver = webdriver.Firefox()

def hasNext():
    return len(driver.find_elements_by_xpath('//button[normalize-space()="Next"]')) == 1

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

#APPLY THROUGH EACH JOB
i = 1
for job in jobList:
    print(i)
    job.click()
    driver.find_element_by_class_name("jobs-apply-button").click()
    while (hasNext()):
        clickNext()
    time.sleep(waitTime)
    #driver.find_element_by_xpath("//div[@class='jobs-apply-button--top-card']/button[@class='jobs-apply-button artdeco-button']").click()
    print(job.text + "\n")
    driver.execute_script("window.scrollTo(0, 100)")
    i += 1