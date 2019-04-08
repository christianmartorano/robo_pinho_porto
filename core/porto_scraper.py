from selenium import webdriver
from helpers import find_element
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from datetime import date

from helpers import socket_windev
from helpers import database_management

import time
import os
import unidecode

CLIENTE_DADOS   = {}

ELEMENTS_SEARCH = {
    "sinistro":"",
    "anoSinistro":"",
}

ELEMENTS_DOSSIE = {
    "XPATH":'//*[@id="frame_91"]',
    "NAME":"tmp",
    "ID":"btn_Dossie"
}

ERROR_MESSAGES = [
    'O SINISTRO PORTO ALUGUEL NÃO FOI ENCONTRADO.',
    'NENHUM DADO FOI ENCONTRADO.'
]

def search_sinistro(driver):
    try:
        driver.switch_to.default_content()
    except TimeoutException as e:
        socket_windev.client_socket('TIM')
        exit()    
    for k, e in ELEMENTS_SEARCH.items():
        ELEMENTS_SEARCH[k] = find_element.find_element(driver, k, "NAME")

def query_sinistro(driver, sinistro, ano):
    ELEMENTS_SEARCH["sinistro"].send_keys(sinistro)
    ELEMENTS_SEARCH["anoSinistro"].send_keys(ano)
    ELEMENTS_SEARCH["sinistro"].send_keys(Keys.ENTER)
    time.sleep(0.5)
    ELEMENTS_SEARCH["sinistro"].clear()
    ELEMENTS_SEARCH["anoSinistro"].clear()

def search_dossie(driver, sinistro):
    for k, e in ELEMENTS_DOSSIE.items():
        element = find_element.find_element(driver, e, k)
        if k == "XPATH":
            driver.switch_to.frame(element)
            time.sleep(1)
            error = find_element.find_element(driver, '//*[@id="corpoMensagem"]', "XPATH")
            if  ERROR_MESSAGES.count(error.text.upper().lstrip().rstrip()) > 0:
                print('Sinistro {} não foi encontrado'.format(sinistro))
                return False
        else:
            driver.execute_script("arguments[0].click();", element)
            time.sleep(1)
    return True

def check_if_exist_greater_than_one_client(driver):
    #Vai até aba Garantidos
    element = find_element.find_element(driver, '//*[@id="container-1"]/ul/li[2]/a/span/img', "XPATH")
    driver.execute_script("arguments[0].click();", element)
    time.sleep(0.5)
    try:
        qtd_paginas = driver.find_element(By.XPATH, '//*[@id="dossieRefPessPaginar"]/table[2]/tbody/tr/td[2]/strong')
        qtd_paginas = qtd_paginas.text.strip().split(" ")[-1]

    except NoSuchElementException as e:
        qtd_paginas = 1
    return int(qtd_paginas)

def scrap_dados(sinistro, ano_sinistro, driver):
    cliente = {
        "endereco":'//*[@id="fragment-1"]/table[1]/tbody/tr[2]/td[2]/table/tbody/tr[5]/td[2]',
        "nome_garantidos":'//*[@id="garantidos"]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]',
        "cpf_garantidos":'//*[@id="garantidos"]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]',
        "indenizacao":'//*[@id="fragment-4"]/table[1]/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]',
        "total_recuperado":'//*[@id="fragment-4"]/table[1]/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]',
        "despesas":'//*[@id="fragment-4"]/table[1]/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td[4]',
        "saldo_a_ressarcir":'//*[@id="fragment-4"]/table[1]/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[4]',
        "total_pago":'//*[@id="fragment-4"]/table[1]/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td[6]'}
    elements = [
            #Aba Garantidos
            '//*[@id="container-1"]/ul/li[2]/a/span/img',
            #Aba Pagamentos
            '//*[@id="container-1"]/ul/li[4]/a/span/img']
    qtd_paginas = check_if_exist_greater_than_one_client(driver)
    for i in range(qtd_paginas):
        element = find_element.find_element(driver, '//*[@id="container-1"]/ul/li[1]/a/span/img', "XPATH")
        driver.execute_script("arguments[0].click();", element)
        time.sleep(1)
        global CLIENTE_DADOS
        for k, c in cliente.items():
            if i > 0 and qtd_paginas > 1 and k != 'nome_garantidos' and k != 'cpf_garantidos':
                    continue
            if k == 'nome_garantidos' or k == 'indenizacao':
                if k == 'nome_garantidos':
                    element = find_element.find_element(driver, elements[0], "XPATH")
                elif k == 'indenizacao':
                    element = find_element.find_element(driver, elements[1], "XPATH")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(1)
                if qtd_paginas > 1 and i > 0 and k == 'nome_garantidos':
                    button = find_element.find_element(driver, '//*[@id="dossieRefPessPaginar"]/table[2]/tbody/tr/td[2]/img[3]', "XPATH")
                    driver.execute_script("arguments[0].click();", button)
                    time.sleep(1)
            element = find_element.find_element(driver, cliente[k], "XPATH")
            CLIENTE_DADOS[k] = element.text.upper()

        database_management.insert_dados(CLIENTE_DADOS, sinistro, ano_sinistro)

def main(driver):
    linha   = 0
    cliente = {}
    driver.switch_to.window(driver.window_handles[-1])
    qtd = database_management.count_cliente()
    socket_windev.client_socket('QTD|{}'.format(qtd))
    res = database_management.select_cliente()

    for row in res.fetchall():
        linha += 1
        print("{} - Capturando sinistro {} ano {}".format(linha, row[0], row[1]))
        search_sinistro(driver)
        query_sinistro(driver, row[0], row[1])
        if search_dossie(driver, row[0]):
            scrap_dados(row[0], row[1], driver)
        socket_windev.client_socket('ACK')
        database_management.update_cliente_exportado(row[0], row[1])
