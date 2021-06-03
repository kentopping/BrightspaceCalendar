import csv
import re
from os import path
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class BrightSpace(object):
    def __init__(self):
        self.PATH = "chromedriver"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(self.PATH, options=chrome_options)
        self.Theory_list = []
        self.Lab_list = []
        self.Due_list = []
        self.courseCodes = []
        self.setCourses()

    def setCourses(self):
        self.courseCodes.append("CST8276_013")
        self.courseCodes.append("CST8276_010")
        self.courseCodes.append("CST8277_300")
        self.courseCodes.append("CST8277_303")
        self.courseCodes.append("CST8334_300")



    def send_keys(self, element_id, keys):
        textbox = self.driver.find_element_by_id(element_id)
        textbox.send_keys(keys)
        time.sleep(2)

    def button_click(self, element_id):
        button = self.driver.find_element_by_link_text(element_id)
        button.click()

    def driver_click(self, element_id):
        try:
            element = WebDriverWait(self.driver, 1).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
            element.click()

        finally:
            time.sleep(3)

    def check(self, course):
        code = course.split()
        code = code[0]
        code = code.split("_")
        code = f"{code[1]}_{code[2]}"
        for i in self.courseCodes:
            if code == i:
                return True
            else:
                continue
        return False

    def sort(self, array):
        for x in array:
            if re.match(r"\d{1,2}:\d{2}\sPM", x):
                time = x.split(":")
                hour = int(time[0])
                hour += 12
                time[0] = str(hour)
                time = f"{time[0]}:{time[1]}"
                x = time
            if re.match(r'\w{4}\w{3}\d{4}.*', x):
                check = self.check(x)
                if check:
                    if "Lab" in x and "Due" not in x:
                        self.Lab_list.append(array.copy())
                        break
                    else:
                        self.Theory_list.append(array.copy())
                        break
            elif "Due" in x:
                self.Due_list.append(array.copy())
                break

    def read_csv(self, name):
        if path.exists(f"{name}.csv"):
            file = open(f"{name}.csv", "r")
            return file

    def write_to_csv(self, list_name, name, month, year):
        if path.exists(f"{name}.csv"):
            file = open(f"{name}.csv", "a", newline="")
        else:
            file = open(f"{name}.csv", "w", newline="")

        writer = csv.writer(file)
        for e in list_name:
            reg = re.match(r"\d{1,2}:\d{2}\s\w{2}", e[2])
            if reg:
                e[1], e[2] = e[2], e[1]

            e.insert(0, month)
            e.insert(0, year)
            new_tup = tuple(e)
            writer.writerow(new_tup)
        list_name.clear()
        file.close()

    def get_info(self):
        Dates = self.driver.find_elements_by_xpath("//div[@class ='d2l-le-calendar-month-day']")
        Date = self.driver.find_element_by_xpath("//h2[@class ='d2l-heading vui-heading-2 d2l-heading-half']")
        Date = Date.text
        date = Date.split()
        month = date[0]
        year = date[1]
        array = []
        for elem in Dates:
            array.append(elem.text)
        # iterating through days
        count = 0
        for elem in array:
            string_array = elem.split('\n')
            Date_num = string_array[0]
            if count == 0 and Date_num != '1':
                continue
            count += 1
            if count > 1 and Date_num == '1':
                break
            num = len(string_array)
            if num != 1:
                if num > 4:
                    string_array.pop(0)
                    test_array = []
                    counter = 0
                    # adding to csv for day
                    for i in string_array:
                        # come back to add the format of the lecture
                        if i != "Zoom Online Meeting":
                            test_array.append(i)
                        counter += 1
                        if counter % 3 == 0:
                            test_array.insert(0, Date_num)
                            self.sort(test_array)
                            test_array.clear()
                else:
                    self.sort(string_array)

        self.write_to_csv(self.Theory_list, "Theory", month, year)
        self.write_to_csv(self.Lab_list, "Labs", month, year)
        self.write_to_csv(self.Due_list, "Assignments", month, year)
        self.driver.find_element_by_xpath(
            "//a[@class ='d2l-iterator-button d2l-iterator-button-next d2l-iterator-button-notext']").click()
        # driver.close()

    def start(self, algonquin_email, algonquin_password):
        self.driver.get('https://brightspace.algonquincollege.com/')
        self.send_keys('i0116', algonquin_email)
        self.driver_click('idSIButton9')
        self.send_keys('passwordInput', algonquin_password)
        self.driver_click('submitButton')
        self.driver_click('idSIButton9')
        self.button_click('Calendar')
        for i in range(0, 4):
            self.get_info()
            time.sleep(5)
        self.driver.close()

