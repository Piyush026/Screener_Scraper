from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

DIRECTORY = 'reports'

BASE_URL = "https://www.screener.in/screen/raw/?sort=&order=&source=&query=Sales+%3E+-10000000000&limit=100"

USERNAME = "fiban98106@pidouno.com"
user = "lilavid669@xhypm.com"
user1 = 'kicij69638@questza.com'
user2 = 'waxam85409@tdcryo.com'
user3 = 'ligepe5611@dkt1.com'
user4 = 'bosova7932@questza.com'
user5 = 'votigo6214@questza.com'
user6 = 'mikic42574@tdcryo.com'
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


def get_driver(options):
    return ChromeDriverManager(options)


HEADER = ["", "Sales-", "Sales Growth %", "Expenses-", "Material Cost %", "Manufacturing Cost %", "Employee Cost %",
          "Other Cost %", "Operating Profit", "OPM %", "Other Income", "Interest", "Depreciation",
          "Profit before tax", "Tax %", "Net Profit", "EPS in Rs", "Dividend Payout %", "Share Capital-",
          "Equity Capital", "Reserves", "Borrowings", "Other Liabilities-", "Trade Payables",
          "Other liability items",
          "Total Liabilities", "Fixed Assets-", "Gross Block", "Accumulated Depreciation", "CWIP", "Investments",
          "Other Assets-", "Inventories", "Trade receivables", "Cash Equivalents", "Loans n Advances",
          "Other asset items",
          "Total Assets", "company_id", "Preference Capital", "Non controlling int", "Advance from Customers"]
