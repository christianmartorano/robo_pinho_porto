from selenium import webdriver
from helpers import find_element

ELEMENTS = {
    "NAME":["login",
            "menu' marginwidth="],
    "XPATH":"/html/body/form/table[2]/tbody/tr[2]/td[2]/a",
    "CLASS_NAME":"stymod"
}

def find_switch_click(driver):
    for k, i in ELEMENTS.items():
        if k == "NAME":
            for i_array in i:
                iframe = find_element.find_element(driver, i_array, k)
                driver.switch_to.frame(iframe)
        else:
            button = find_element.find_element(driver, i, k)
            driver.execute_script("arguments[0].click();", button)
