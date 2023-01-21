import self as self

import XLutils
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
import time

s = Service(r"C:\Users\saikr\PycharmProjects\selenium_firstclass\drivers\chromedriver.exe/chromedriver.exe")
driver = webdriver.Chrome(service=s)
# driver = webdriver.Chrome(r"C:\Users\saikr\PycharmProjects\selenium_firstclass\drivers\chromedriver.exe/chromedriver.exe")
url = r"https://igs.imarticus.org/stratonboardportal/uatinternal/"
# url=r"https://practicetestautomation.com/practice-test-login/"
driver.get(url)
driver.maximize_window()
action = ActionChains(driver)
path = r"C:\Users\saikr\Downloads\user_creation_data.xlsx"
rows = XLutils.getRowcount(path, "Sheet1")

# workspace selection UI
driver.find_element(By.XPATH, "//span[@class='select2-selection__arrow']").click()
time.sleep(2)
driver.find_element(By.XPATH, "//input[@type='search']").send_keys("Sample Workspace")  # entered workspace name
time.sleep(2)
driver.find_element(By.XPATH, "//span[text()=' Sample Workspace']").click()
time.sleep(2)
driver.find_element(By.XPATH, "//button[text()='Next']").click()
time.sleep(2)
driver.find_element(By.XPATH, "(//a[@id='fedlogin'])[1]").click()
time.sleep(2)

# login UI
driver.find_element(By.XPATH, "(//input[@id='signInFormUsername'])[2]").send_keys("varun.paladugula@imarticus.com")
driver.implicitly_wait(5)
driver.find_element(By.XPATH, "(//input[@id='signInFormPassword'])[2]").send_keys('Password@22')
driver.implicitly_wait(5)
driver.find_element(By.XPATH, "(//input[@name='signInSubmitButton'])[2]").click()
driver.implicitly_wait(5)

# entered into Authoring Engine
# now configuring the game
driver.find_element(By.XPATH, "//span[text()='Configurations']").click()
time.sleep(2)
driver.find_element(By.XPATH, "//p[text()='User Management']").click()
time.sleep(2)
driver.find_element(By.XPATH, "//a[text()='Manage Users']").click()
time.sleep(2)

# creating a loop to create different users in a workspace
# using data in an Excel sheet
for r in range(2, rows+1):
    # creating user
    driver.find_element(By.XPATH, "//a[@class='btn orange_btn']").click()
    time.sleep(2)

    # reading data from excel
    First_Name = XLutils.readData(path, "Sheet1", r, 2)
    Nick_Name = XLutils.readData(path, "Sheet1", r, 3)
    Email_Id = XLutils.readData(path, "Sheet1", r, 4)
    #Password = XLutils.readData(path, "Sheet1", r, 5)

    # entering data
    driver.find_element(By.XPATH, "//input[@id='FIRST_NAME']").send_keys(First_Name)
    #firstname textfield only accepts alpahbets
    time.sleep(2)
    driver.find_element(By.XPATH, "//input[@id='NICK_NAME']").send_keys(Nick_Name)
    time.sleep(2)

    # authentication type dropp down
    authentication_type = driver.find_element(By.XPATH, "//select[@id='AUTHTYPE']")
    type=Select(authentication_type)
    type.select_by_index(1) #since we are selecting cognito , password textfiled will disappaer
    time.sleep(2)

    #email_id should be unique
    driver.find_element(By.XPATH, "//input[@id='EMAIL_ID']").send_keys(Email_Id)
    time.sleep(2)
    # driver.find_element(By.XPATH, "//input[@id='PASSWORD']").send_keys(Password) #no need of password if cognito, sample workspace
    # time.sleep(2)

    # radio button
    driver.find_element(By.XPATH, "(//input[@name='IS_COMPETITOR'])[2]").click()  # clicking 'no'
    time.sleep(2)

    # workspace role drop down
    workspace_role = driver.find_element(By.XPATH, "//select[@name='WS_ROLE_ID']")
    wrole=Select(workspace_role)
    wrole.select_by_visible_text("SAMPLE ROLE")  # given role as 'sample role'
    time.sleep(2)

    # portal role
    driver.find_element(By.XPATH, "//input[@class='select2-search__field']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//li[@class='select2-results__option select2-results__option--highlighted']").click()
    time.sleep(2)

    # adding user by clicking add
    driver.find_element(By.XPATH, "// input[ @ type = 'submit']").click()

    XLutils.writeData(path, "Sheet1", r, 6, "created")
    time.sleep(2)

    # going back
    driver.find_element(By.XPATH, "//a[@class='btn orange_btn float-end waves-effect waves-light px-4']").click()
    time.sleep(2)

driver.close()
