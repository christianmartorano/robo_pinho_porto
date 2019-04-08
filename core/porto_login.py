from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from helpers import find_element
from helpers import database_management
from helpers import socket_windev

import time

#Variáveis Globais
ELEMENTS = {
    "webusrcod":"",
    "webusrshn":"",
    "B1":"submit"
}

def send_keys(element, text):
    if text == "submit":
        element.submit()
    else:
        element.send_keys(text)

def login(driver):

    res = database_management.usuario_senha()
    url = res[2]

    ELEMENTS["webusrcod"] = res[0]
    ELEMENTS["webusrshn"] = res[1]

    try:
        driver.get(url)
    except TimeoutException as e:
        socket_windev.client_socket('TIM')
        exit()
    #Troca para o Iframe
    iframe = find_element.find_element(driver, "login", "NAME")
    driver.switch_to.frame(iframe)
    for e, t in ELEMENTS.items():
        element = find_element.find_element(driver, e, "NAME")
        send_keys(element, t)
    driver.switch_to.default_content()
