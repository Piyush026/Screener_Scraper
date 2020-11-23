from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
DIRECTORY = 'reports'

BASE_URL = "https://www.screener.in/screen/raw/?sort=&order=&source=&query=Sales+%3E+-10000000000&limit=100"

USERNAME = "fiban98106@pidouno.com"
PASSWORD = "Jack@123"
WEB = 'https://www.screener.in'

def get_chrome_web_driver(options):
    return webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)


def get_web_driver_options():
    return webdriver.ChromeOptions()


def set_ignore_certificate_error(options):
    options.add_argument('--ignore-certificate-errors')


def set_browser_as_incognito(options):
    options.add_argument('--incognito')


def set_browser_in_fullScreen(options):
    options.add_argument("--start-maximized")


def set_automation_as_head_less(options):
    options.add_argument('--headless')
