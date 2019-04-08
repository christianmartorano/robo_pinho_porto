#!/usr/bin/env python
try:
  from selenium import webdriver
except Exception as e:
    print("Necessário instalar biblioteca selenium")

from core import porto_login
from core import porto_login_gerenciador
from core import porto_scraper

from helpers import socket_windev
from helpers import database_management

import sys

BANNER = '''
  _____   ____  _____ _______ ____    _____ _____ _   _ _    _  ____   
 |  __ \ / __ \|  __ \__   __/ __ \  |  __ \_   _| \ | | |  | |/ __ \  
 | |__) | |  | | |__) | | | | |  | | | |__) || | |  \| | |__| | |  | | 
 |  ___/| |  | |  _  /  | | | |  | | |  ___/ | | | . ` |  __  | |  | | 
 | |    | |__| | | \ \  | | | |__| | | |    _| |_| |\  | |  | | |__| | 
 |_|     \____/|_|  \_\ |_|  \____/  |_|   |_____|_| \_|_|  |_|\____/  '''

def main():

    database_management.main()

    with webdriver.Chrome() as driver:

        driver.set_page_load_timeout(30)
        porto_login.login(driver)
        porto_login_gerenciador.find_switch_click(driver)
        porto_scraper.main(driver)
        socket_windev.client_socket('FIN')

    database_management.fecha_conexao()

    input("PROCESSO FINALIZADO COM SUCESSO.\rPRESSIONE QUALQUER TECLA PARA FECHAR.")

if __name__ == "__main__":
    print(BANNER)
    main()
