Title:       Canvas-Uploader Instruction
Author:      Shenghao Zou  
Affiliation: University of Wisconsin, Madison 
Date:        Feb, 21 2018

# Canvas-Uploader
## Introduction
This is a simple script to upload your grades stored in excel files to Canvas system. You can use your own excel spreadsheets to track comments, and specific graders for each rubrics. It used selenium and Firefox to simulate user input. It can work on Windows, Mac OS X and Linux systems.

## Install & Run
To install and run this script, you should firstly install Python 2, selenium, Firefox and geckodriver. (In the past, we used Chrome and chromedriver but it seems sometimes Chrome didn't work very well).
1. To install selenium, please run `pip install selenium`.
2. To install geckodriver, Please click here: [Gecodriver Releases](https://github.com/mozilla/geckodriver/releases) Please unzip it in any folder you like and add geckodirver path to system PATH variable. Restart terminal and try `which geckodriver` to see if you can access to it.

To run the code, you should first make sure your configuration is correct, then run `python submit_firefox.py [Your Spreadsheet Name].xlsx`. Don't do anything when submitting.

## Configuration
There are several things you should change before running this script:
1. **CANVAS_HOME_PAGE** variable: If you are not a UW-Madison student/faculty, change it to your university's Canvas homepage.
2. **COURSE_CODE** variable: change to your course code. Open your Canvas course homepage. For example, the URL will be:*https://canvas.wisc.edu/courses/91385*. Here, 91385 is the course number.
3. **YOUR_CANVAS_NAME** variable: Your first name on Canvas.
4. **DELETE_COMMENT** variable: By default delete comment feature will be on. It will deletes repeated comments by you. Sometimes, the script will fail and it can help you to avoid multiple same comments. If you don't need this feature, please set this to 0.

## Excel File Format
Please take a look of my example.xlsx file for more information. The script need Student ID for matching. To get that, you can export a csv file from Canvas Grade page and you can find SID there.
