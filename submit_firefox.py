# Copyright (c) 2017, Shenghao Zou from University of Wisconsin, Madison
# All rights reserved.

import selenium
import unicodedata
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
from openpyxl import load_workbook
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from getpass import getpass

# Change variables here!
YOUR_CANVAS_NAME = 'Frank'
COURSE_CODE = '91385'
CANVAS_HOME_PAGE = "https://canvas.wisc.edu"
DELETE_COMMENT = 1

def student_submit(drv, assignment, sid, points, comments):
    global wait
    global DELETE_COMMENT
    if isinstance(comments, unicode):
        comments = unicodedata.normalize('NFKD', comments).encode('ascii','ignore')
    elif not isinstance(comments, str):
        comments = ''
    drv.get(CANVAS_HOME_PAGE + '/courses/{2}/gradebook/speed_grader?assignment_id={0}#%7B%22student_id%22%3A%22{1}%22%7D'.format(assignment, sid, COURSE_CODE))
    #print 'Please Confirm Login and Load.'
    #a = input()
    #time.sleep(1)
    view_rubric = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, VIEW_RUBRIC_SELECTOR)))
    pts = drv.find_elements_by_css_selector(POINTS_SELECTOR)
    # view_rubric = drv.find_element_by_css_selector(VIEW_RUBRIC_SELECTOR)
    comment = drv.find_element_by_id(COMMENT_ID)
    submit = drv.find_element_by_id(SUBMIT_ID)
    total_grade = drv.find_element_by_id(TOTAL_GRADE_SELECTOR)
    view_rubric.click()
    save = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, SAVE_SELECTOR)))
    i = 0
    for x in points:
        pts[i].clear()
        pts[i].send_keys(str(x))
        i = i + 1
    total_grade.send_keys(str(sum(points)))
    comment_delete = drv.find_elements_by_css_selector(DELETE_ASSIGNMENT_SELECTOR)
    if DELETE_COMMENT:
        for deletes in comment_delete:
            res = deletes.get_attribute('innerHTML').encode('ascii','ignore')
            if YOUR_CANVAS_NAME in res or 'FRANK' in res:
                deletes_x = deletes.find_element_by_css_selector('.delete_comment_link.icon-x')
                deletes_x.click()
                wait.until(EC.alert_is_present())
                alert = drv.switch_to.alert
                alert.accept()

    if comments != None:
        comment.send_keys(comments)
    #print 'comfirm'
    #a = raw_input()
    save.click()
    submit.click()
    # time.sleep(1)

USER_NAME = 'szou28' # Please change it to your own user name.

print 'USER:',USER_NAME
print 'Please enter the password:'
USER_PWD = getpass()
print 'Saved.'
TESTS_NUM = int(raw_input('How many rubrics do we have (a number for example 8): '))
assignment = int(raw_input('Please enter the assignment ID (for example 199326): '))

if len(sys.argv) <= 1:
    print 'please give me the file name(WITH .xlsx): '
    fileName = raw_input()
else:
    fileName = sys.argv[1]
print 'You are now submitting assignment id = ' + str(assignment) + ' test rubrics number:' + str(TESTS_NUM) + ' filename:' + fileName
y = raw_input('confirm? \nPlease enter \'y\' to confirm your submission. \nDon\'t do anything when submitting: ')
if y != 'y':
    exit()

driver = webdriver.Firefox()
driver.get(CANVAS_HOME_PAGE)
driver.maximize_window()
print 'Login.'
POINTS_SELECTOR = '.criterion_points.span1.no-margin-bottom'
VIEW_RUBRIC_SELECTOR = '.toggle_full_rubric.edit.btn'
COMMENT_ID = 'speedgrader_comment_textarea'
SUBMIT_ID = 'comment_submit_button'
SAVE_SELECTOR = '.save_rubric_button.Button.Button--primary'
DELETE_ASSIGNMENT_SELECTOR = '.comment'
TOTAL_GRADE_SELECTOR = 'grading-box-extended'
first_rubric = 1

wait = WebDriverWait(driver, 45)
USER_NAME_ID = 'j_username'
USER_PASSWORD_ID = 'j_password'
SUBMIT_LOGIN_NAME = '_eventId_proceed'

SID_COL = 'B'
COM_COL = 'C'
TEST_COL = 'D'


submit = wait.until(EC.element_to_be_clickable((By.NAME, SUBMIT_LOGIN_NAME)))
username = driver.find_element_by_id(USER_NAME_ID)
pwd = driver.find_element_by_id(USER_PASSWORD_ID)
username.send_keys(USER_NAME)
pwd.send_keys(USER_PWD)
submit.click()


print 'loading files from ' + fileName
wb = load_workbook(fileName)
worksheet = wb[wb.get_sheet_names()[0]]

i = 2
first = 1
while True:
    sid = worksheet[SID_COL + str(i)].value
    if sid == None:
        break
    points = [worksheet[chr(ord(TEST_COL) + t) + str(i)].value for t in range(TESTS_NUM)]
    comments = worksheet[COM_COL + str(i)].value
    print sid
    print points
    print comments
    i = i + 1
    time.sleep(1)
    student_submit(driver, assignment, str(sid), points, comments)

driver.quit()
