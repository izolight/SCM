#!/usr/bin/env python3

from selenium import webdriver
import string, random


def id_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


data = id_generator()

driver = webdriver.Chrome()

driver.get("http://localhost:8080/members/add")
first_name = driver.find_element_by_id("first_name")
last_name = driver.find_element_by_id("last_name")
user_name = driver.find_element_by_id("username")
address = driver.find_element_by_id("address")
city = driver.find_element_by_id("city")
zip_code = driver.find_element_by_id("zip_code")
email = driver.find_element_by_id("email")
password1 = driver.find_element_by_id("password1")
password2 = driver.find_element_by_id("password2")

first_name.send_keys('test')
last_name.send_keys('user')
address.send_keys('teststrasse')
user_name.send_keys(data)
city.send_keys('bern')
zip_code.send_keys('3000')
email.send_keys(data + '@user.com')
password1.send_keys(data)
password2.send_keys(data)

driver.find_element_by_id("submit-add-member").click()
