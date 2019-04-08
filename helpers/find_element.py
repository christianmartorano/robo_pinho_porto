from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from helpers import socket_windev
import time

def find_element(driver, element, search):
    time.sleep(0.5)
    if search == "NAME":
        try:
            element = driver.find_element(By.NAME, element)
        except NoSuchElementException as e:
            socket_windev.client_socket('ERR')
    elif search == "XPATH":
        try:
            element = driver.find_element(By.XPATH, element)
        except NoSuchElementException as e:
            socket_windev.client_socket('ERR')
    elif search == "ID":
        try:
            element = driver.find_element(By.ID, element)
        except NoSuchElementException as e:
            socket_windev.client_socket('ERR')
    else:
        try:
            element = driver.find_element(By.CLASS_NAME, element)
        except NoSuchElementException as e:
            socket_windev.client_socket('ERR')
    return element
