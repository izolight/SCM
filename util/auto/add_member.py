#!/usr/bin/env python3

from selenium import webdriver
import string, random


def id_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


data = id_generator()

driver = webdriver.Chrome()

driver.get("http://localhost:8000/members/add")
first_name = driver.find_element_by_id("id_first_name")
last_name = driver.find_element_by_id("id_last_name")
user_name = driver.find_element_by_id("id_username")
address = driver.find_element_by_id("id_address")
city = driver.find_element_by_id("id_city")
zip_code = driver.find_element_by_id("id_zip_code")
email = driver.find_element_by_id("id_email")
phone_number = driver.find_element_by_id("id_phone_number")
password1 = driver.find_element_by_id("id_password1")
password2 = driver.find_element_by_id("id_password2")

first_name.send_keys('test')
last_name.send_keys('user')
address.send_keys('teststrasse')
user_name.send_keys(data)
city.send_keys('bern')
zip_code.send_keys('3000')
email.send_keys(data + '@user.com')
phone_number.send_keys("+41123456789")
password1.send_keys(data)
password2.send_keys(data)

driver.find_element_by_id("submit-add-member").click()
