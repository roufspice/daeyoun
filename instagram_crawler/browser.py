import os

from selenium import webdriver


# 내장 패키지 import
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class Browser:

    def __init__(self, has_screen):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        service_args = ["--ignore-ssl-errors=true"]
        chrome_options = Options()
        if not has_screen:
            chrome_options.add_argument("--headless")

        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(
            executable_path= f'{dir_path}/bin/chromedirver',
            service_args=service_args,
            chrome_options=chrome_options
        )
        self.driver.implicitly_wait(5)



    def page_height(self):
        return  self.driver.execute_script("return document.body.scrollHeight")

    def get(self, url):
        self.driver.get(url)

    def current_url(self):
        return self.driver.current_url

    def implicity_wait(self, time):
        self.driver.implicitly_wait(time)

    def find_one(self, css_selector, elem=None, waittime=0):
        obj = elem or self.driver

        if waittime:
            WebDriverWait(obj, waittime).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, css_selector)))


        try:
            return obj.find_element(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return None


    def find(self, css_selector, elem=None, waittime=0):
        obj = elem or self.driver

        try:
            if waittime:
                WebDriverWait(obj,waittime).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

        except TimeoutException:
            return None


        try:
            return obj.find_elements(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return None


    def scroll_down(self, wait=0.2):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        randmized_sleep(wait)


    def scroll_up(self, offset=-1, wait=2):
        if offset == -1:
            self.driver.execute_script("window.scrollTo(0,0)")

        else:
            self.driver.execute_script("window.scrollBy(0, -%s)" % offset)
        randmized_sleep(wait)


    def js_click(self, elem):
        self.driver.execute_script("arguments[0].click();", elem)

    def open_new_tab(self, url):
        self.driver.execute_script("window.open('%s');" %url)
        self.driver.switch_to.window(self.driver.window_handles[1])

    def close_current_tab(self):
        self.driver.close()

        self.driver.switch_to.window(self.driver.window_handles[0])

    def __del__(self):
        try:
            self.driver.quit()
        except Exception:
            pass




