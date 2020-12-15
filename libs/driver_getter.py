import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_driver():
    root_path ='..'
    chrome_options = Options()
    driver = webdriver.Chrome(
        executable_path=f'{root_path}/chrome_driver/chromedriver.exe',
        options=chrome_options
    )

    return driver