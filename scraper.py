from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import re
import pandas as pd
import random
import time
from bs4 import BeautifulSoup
from scraper_config import (
    get_web_driver_options,
    get_chrome_web_driver,
    set_browser_as_incognito,
    set_ignore_certificate_error,
    set_browser_in_fullScreen,
    set_automation_as_head_less,
    USERNAME,
    PASSWORD,
    DIRECTORY,
    BASE_URL,
    WEB,
)


class Reporter:

    def __init__(self, base_url):
        self.base_url = base_url
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        set_browser_in_fullScreen(options)
        self.driver = get_chrome_web_driver(options)

    def run(self):
        print("starting Script")
        self.driver.get(self.base_url)
        pause = random.randint(5, 7)
        print(f"Sleeping for {pause}...")
        time.sleep(pause)
        self.login()

    def login(self):
        print("start login")
        self.driver.find_element_by_xpath("/html/body/nav/div[1]/div/div[1]/div[3]/div[2]/a[1]").click()
        self.driver.find_element_by_xpath('//*[@id="id_username"]').send_keys(USERNAME)
        self.driver.find_element_by_xpath('//*[@id="id_password"]').send_keys(PASSWORD)
        self.driver.find_element_by_xpath('/html/body/main/div/div/div[2]/form/button').click()
        self.driver.get(self.base_url)
        self.company_links = self.link()

    def results_per_page(self):
        self.driver.find_element_by_xpath("//a[contains(text(),'50')]").click()

    def link(self):
        page = self.driver.page_source
        soup = BeautifulSoup(page, "html.parser")
        table = soup.find('table')
        hrefs = table.find_all('a', href=True)
        links = []
        for x in hrefs:
            if '/' in x['href']:
                links.append(x['href'])
        return links

    def creating_links(self):
        new_list = [WEB + x for x in self.company_links]
        # print(new_list)
        return new_list

    def company_details(self):
        companies = self.creating_links()
        try:
            for company in companies:
                self.driver.get(company)
                time.sleep(2)
                table_name = "quarters"
                self.scroll_element(table_name)
                self.open_sales_expenses(4)
                page = self.driver.page_source
                soup = BeautifulSoup(page, "html.parser")
                data = soup.find_all("table", {"class": "data-table"})
                self.quarterly_results(data[1])
                table_name = "profit-loss"
                self.scroll_element(table_name)
                time.sleep(2)
                self.open_sales_expenses(5)
                page = self.driver.page_source
                soup = BeautifulSoup(page, "html.parser")
                data = soup.find_all("table", {"class": "data-table"})
                self.quarterly_results(data[2])
                time.sleep(2)
                table_name = "balance-sheet"
                self.scroll_element(table_name)
                time.sleep(2)
                page = self.driver.page_source
                soup = BeautifulSoup(page, "html.parser")
                data = soup.find_all("table", {"class": "data-table"})
                self.open_balance_sheet()
                self.quarterly_results(data[3])

        except Exception as e:
            self.driver.save_screenshot("lol.png")
            print(e)

    def quarterly_results(self, gdp):
        table1 = gdp
        body = table1.find_all("tr")
        head = body[0]
        # print(head)
        body_rows = body[1:]
        headings = []
        for item in head.find_all("th"):
            item = item.text.rstrip("\n")
            headings.append(item)
        print(headings)

        all_rows = []
        for row_num in range(len(body_rows)):
            row = []
            for row_item in body_rows[row_num].find_all("td"):
                aa = re.sub("(\xa0)|(\n)|,", "", row_item.text)
                row.append(aa.strip())
            all_rows.append(row)

        print(all_rows)

        df = pd.DataFrame(data=all_rows, columns=headings)
        print(df.head())
        df.to_csv("file1.csv")

    def open_sales_expenses(self, num):
        try:
            time.sleep(1)
            self.driver.find_element_by_xpath(
                f'//body[1]/main[1]/section[{num}]/div[2]/table[1]/tbody[1]/tr[1]/td[1]/button[1]').click()
            time.sleep(2)
            self.driver.find_element_by_xpath(
                f'//body[1]/main[1]/section[{num}]/div[2]/table[1]/tbody[1]/tr[3]/td[1]/button[1]').click()
            time.sleep(3)
        except NoSuchElementException:
            time.sleep(1)
            self.driver.find_element_by_xpath(
                f'//body[1]/main[1]/section[{num}]/div[3]/table[1]/tbody[1]/tr[1]/td[1]/button[1]').click()
            time.sleep(2)
            self.driver.find_element_by_xpath(
                f'//body[1]/main[1]/section[{num}]/div[3]/table[1]/tbody[1]/tr[3]/td[1]/button[1]').click()
            time.sleep(3)

    def scroll_element(self, table):
        time.sleep(2)
        element = self.driver.find_element_by_xpath(f'//*[@id="{table}"]/div[1]/div[1]/h2')
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def open_balance_sheet(self):
        time.sleep(2)
        self.driver.find_element_by_xpath(
            f'//body[1]/main[1]/section[6]/div[2]/table[1]/tbody[1]/tr[1]/td[1]/button[1]').click()
        self.driver.find_element_by_xpath(
            f'//body[1]/main[1]/section[6]/div[2]/table[1]/tbody[1]/tr[4]/td[1]/button[1]').click()
        time.sleep(5)
        self.driver.find_elements_by_class_name("button-plain")[12].click()
        self.driver.find_elements_by_class_name("button-plain")[13].click()
        # self.driver.find_element_by_xpath(
        #     '//*[@id="balance-sheet"]/div[2]/table/tbody/tr[6]/td[1]/button').click()
        # self.driver.find_element_by_xpath(
        #     '//*[@id="balance-sheet"]/div[2]/table/tbody/tr[6]/td[1]/button').click()


def main():
    reporter = Reporter(BASE_URL)
    reporter.run()
    reporter.creating_links()
    reporter.company_details()


if __name__ == '__main__':
    main()
