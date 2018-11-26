import ssl
from configparser import ConfigParser

import wget
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ssl._create_default_https_context = ssl._create_unverified_context


def config(filename='settings.ini', section="learn"):
    parser = ConfigParser()
    parser.read(filename)

    data = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            data[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return data


def get_page(url):
    driver = webdriver.Firefox(executable_path='./geckodriver')
    driver.get(url)
    return driver


def login_github(nick, password, driver):
    login_field = driver.find_element_by_name("login")
    login_field.send_keys(nick)
    password_field = driver.find_element_by_name("password")
    password_field.send_keys(password)
    driver.find_element_by_name("commit").click()


def login(nick, password, driver):
    login_field = driver.find_element_by_id("user-email")
    login_field.send_keys(nick)
    password_field = driver.find_element_by_id("user-password")
    password_field.send_keys(password, Keys.ENTER)


def open_lesson(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "button--color-yellow")))
    driver.find_element_by_class_name("button--color-yellow").click()


def open_github_page(driver):
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'button--icon-only')))
    element.click()


def click_on_js_element(driver, class_name):
    script_string = f"document.getElementsByClassName('{class_name}')[0].click()"
    driver.execute_script(script_string)


def download_file(index, url):
    url_filename = wget.detect_filename(url)
    filename = f'{index}_{url_filename}.zip'
    url = get_download_url(url)
    wget.download(url, out=filename)
    print(f"Downloading {filename} file.")


def get_download_url(url):
    return f'{url}/archive/master.zip'


def last_page_reached(driver):
    return driver.title == config()['last_page_title']


def page_has_loaded(self):
    self.log.info("Checking if {} page is loaded.".format(self.driver.current_url))
    page_state = self.driver.execute_script('return document.readyState;')
    return page_state == 'complete'
