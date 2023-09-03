from copy import Error
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

first_name = 'Your Name'
last_name = 'Your Surname'
country = 'nepal' # don't change this
email = 'youremail@gmail.com'
degree = "Bachelor's in Engineering"
institution = 'Institute of Engineering'
study_years = '4'

titles = []
credits = []
credit_mins = []
grades = []

format = '''
The grade file is in csv format without header. Read Readme file for more:
'''

print(format)
filename = input("Enter path to grade file (leave it empty to be `grade.csv`):")
if not filename:
    filename = 'grade.csv'

with open(filename, encoding="utf-8") as f:
    line = f.readline()
    while line:
        title, credit, credit_min, grade = line.strip().split(',')
        if credit.isnumeric() and credit_min.isnumeric() and grade.isnumeric() and int(credit) > 0:
            titles.append(title)
            credits.append(credit)
            credit_mins.append(credit_min)
            grades.append(grade)
        line = f.readline()

driver = webdriver.Chrome()

driver.get("https://applications.wes.org/igpa-calculator/igpa.asp")
wait = WebDriverWait(driver, 6000)

NetworkErr = False
while True:
    if driver.find_element('xpath', '/html').get_attribute('dir') == "ltr":
        if not NetworkErr:
            print("Network error, please check your network!")
            NetworkErr = True
        driver.get(
            "https://applications.wes.org/igpa-calculator/igpa.asp")
        time.sleep(3)
    else:
        NetworkErr = False
        break

last_name_wait = wait.until(EC.presence_of_element_located((By.ID, "frm_last_name")))
first_name_wait = wait.until(EC.presence_of_element_located((By.ID, "frm_first_name")))
country_wait = wait.until(EC.presence_of_element_located((By.ID, "frm_lst_ctry_residence")))
email_wait = wait.until(EC.presence_of_element_located((By.ID, "frm_email")))
email2_wait = wait.until(EC.presence_of_element_located((By.ID, "frm_email2")))
continue_btn = wait.until(EC.presence_of_element_located((By.ID, "GoToMain_bttn")))

last_name_wait.send_keys(last_name)
first_name_wait.send_keys(first_name)
country_wait.send_keys(country + Keys.ENTER)
email_wait.send_keys(email)
email2_wait.send_keys(email)
continue_btn.click()

degree_name_wait = wait.until(EC.presence_of_element_located((By.NAME, "frm_stud_nm")))
institution_name_wait = wait.until(EC.presence_of_element_located((By.NAME, "frm_inst_nm")))
education_country_wait = wait.until(EC.presence_of_element_located((By.NAME, "frm_lst_ctry")))
degree_name_wait.send_keys(degree)
institution_name_wait.send_keys(institution)
education_country_wait.send_keys(country + Keys.ENTER)

study_years_wait = wait.until(EC.presence_of_element_located((By.NAME, "frm_lst_numyearsem")))
study_years_wait.send_keys(study_years + Keys.ENTER)

terms_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@name="terms_ckbox"]/following-sibling::label')))
terms_checkbox.click()

next_button_wait = wait.until(EC.presence_of_element_located((By.ID, 'trButton')))
next_button_wait.click()

for i in range(1, len(titles)+1):
    title = wait.until(EC.presence_of_element_located((By.ID, "title"+str(i))))
    credit = wait.until(
        EC.presence_of_element_located((By.ID, "credit"+str(i))))
    credit_min = wait.until(EC.presence_of_element_located((By.ID, "credit_min"+str(i))))
    grade = wait.until(EC.presence_of_element_located((By.ID, "num_grd"+str(i))))
    title.send_keys(titles[i-1])
    credit.send_keys(Keys.CONTROL + "A")
    credit.send_keys(Keys.BACKSPACE)
    credit.send_keys(credits[i-1])
    credit_min.send_keys(Keys.CONTROL + "A")
    credit_min.send_keys(Keys.BACKSPACE)
    credit_min.send_keys(credit_mins[i-1])
    grade.send_keys(grades[i-1])
    if i != len(titles):
        driver.execute_script("ShowRow();")
    # time.sleep(0.2)

while True:
    submit = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//input[@value="Calculate GPA"]')))
    submit.click()
# raise Error("Done! Please close the browser manually after reviewing your GPA.")
