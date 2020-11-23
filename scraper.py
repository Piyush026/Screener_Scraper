import sys
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# caps = DesiredCapabilities.CHROME
# caps['goog:loggingPrefs'] = {'performance': 'ALL'}
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
        for company in companies:
            try:
                self.driver.get(company)
                # time.sleep(2)
                # table_name = "quarters"
                # self.scroll_element(table_name)
                # self.open_sales_expenses(4)
                # data = self.parse_page()
                # self.quarterly_results(data[1])
                # table_name = "profit-loss"
                # self.scroll_element(table_name)
                # self.open_sales_expenses(5)
                # data = self.parse_page()
                # self.quarterly_results(data[2])
                # time.sleep(2)
                # table_name = "balance-sheet"
                # self.scroll_element(table_name)
                # time.sleep(2)
                # self.open_balance_sheet()
                # data = self.parse_page()
                # self.quarterly_results(data[3])
                # time.sleep(2)
                # table_name = "shareholding"
                # self.scroll_element(table_name)
                # self.open_shareholding()
                # time.sleep(2)
                # data = self.parse_page()
                # self.quarterly_results(data[6])
                """basic info"""
                self.basic_info()
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print("line->" + str(exc_tb.tb_lineno))
                print('Exception occurred in complete_details() method->' + str(e))
                self.driver.save_screenshot("lol.png")
                continue

    def parse_page(self):
        page = self.driver.page_source
        soup = BeautifulSoup(page, "html.parser")
        data = soup.find_all("table", {"class": "data-table"})
        print(data)
        return data

    cnt = 0

    def quarterly_results(self, gdp):
        table1 = gdp
        body = table1.find_all("tr")
        head = body[0]
        body_rows = body[1:]
        headings = []
        for item in head.find_all("th"):
            item = item.text.rstrip("\n")
            headings.append(item)
        all_rows = []
        for row_num in range(len(body_rows)):
            row = []
            for row_item in body_rows[row_num].find_all("td"):
                aa = re.sub("(\xa0)|(\n)|,", "", row_item.text)
                row.append(aa.strip())
            all_rows.append(row)
        df = pd.DataFrame(data=all_rows, columns=headings)
        print(df.head())
        df.to_csv("file1.csv")
        return df

    def open_sales_expenses(self, num):
        try:
            time.sleep(1)
            self.driver.find_element_by_xpath(
                f'//body[1]/main[1]/section[{num}]/div[2]/table[1]/tbody[1]/tr[1]/td[1]/button[1]').click()
            time.sleep(2)
            self.driver.find_element_by_xpath(
                f'//body[1]/main[1]/section[{num}]/div[2]/table[1]/tbody[1]/tr[3]/td[1]/button[1]').click()
            time.sleep(1)
        except NoSuchElementException:
            time.sleep(1)
            self.driver.find_element_by_xpath(
                f'//body[1]/main[1]/section[{num}]/div[3]/table[1]/tbody[1]/tr[1]/td[1]/button[1]').click()
            time.sleep(2)
            self.driver.find_element_by_xpath(
                f'//body[1]/main[1]/section[{num}]/div[3]/table[1]/tbody[1]/tr[3]/td[1]/button[1]').click()
            time.sleep(1)

    def scroll_element(self, table):
        try:
            time.sleep(1)
            element = self.driver.find_element_by_xpath(f'//*[@id="{table}"]/div[1]/div[1]/h2')
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        except NoSuchElementException:
            time.sleep(1)
            self.driver.find_element_by_xpath("/html/body/nav/div[2]/div/div/a[10]").click()

    def open_balance_sheet(self):
        time.sleep(2)
        self.driver.find_element_by_xpath(
            f'//body[1]/main[1]/section[6]/div[2]/table[1]/tbody[1]/tr[1]/td[1]/button[1]').click()
        self.driver.find_element_by_xpath(
            f'//body[1]/main[1]/section[6]/div[2]/table[1]/tbody[1]/tr[4]/td[1]/button[1]').click()
        time.sleep(2)
        self.driver.find_elements_by_class_name("button-plain")[11].click()
        time.sleep(2)
        self.driver.find_elements_by_class_name("button-plain")[12].click()
        time.sleep(1)

    def open_shareholding(self):
        try:
            try:
                time.sleep(1)
                data = self.driver.find_element_by_xpath(
                    "//*[contains(text(), 'FIIs')]").text
                if data:
                    self.driver.find_element_by_xpath(
                        "//*[contains(text(), 'FIIs')]").click()
                time.sleep(1)
                diis = self.driver.find_element_by_xpath(
                    "//*[contains(text(), 'DIIs')]").text
                if diis:
                    self.driver.find_element_by_xpath(
                        "//*[contains(text(), 'DIIs')]").click()
                    time.sleep(1)
            except NoSuchElementException:
                time.sleep(1)
                diis = self.driver.find_element_by_xpath(
                    "//*[contains(text(), 'DIIs')]").text
                if diis:
                    self.driver.find_element_by_xpath(
                        "//*[contains(text(), 'DIIs')]").click()
                    time.sleep(1)

            self.driver.find_elements_by_xpath(
                "//*[contains(text(), 'Promoters')]")[1].click()
            self.driver.find_element_by_xpath(
                "//*[contains(text(), 'Public')]").click()

        except:
            time.sleep(2)
            self.driver.find_element_by_xpath(
                "//*[contains(text(), 'Promoters')]").click()
            self.driver.find_element_by_xpath(
                "//*[contains(text(), 'Public')]").click()
        try:
            time.sleep(2)
            self.driver.find_element_by_xpath(
                "//*[contains(text(), 'Government')]").click()
        except:
            pass

    info = {}

    def basic_info(self):
        name = self.driver.find_element_by_xpath('//*[@id="top"]/div[1]/h1').text
        link = self.driver.find_element_by_xpath('//*[@id="top"]/div[2]/a[1]/span').text
        code = self.driver.find_element_by_xpath('//*[@id="top"]/div[2]/a[2]/span').text
        bse = code.replace("BSE:", '').strip()
        sub = self.driver.find_element_by_class_name("company-profile-about").text
        about = sub.replace("ABOUT\n", '')
        nse = self.nse()
        sector = self.driver.find_element_by_xpath('//*[@id="peers"]/div[1]/div[1]/p/a[1]').text
        industry = self.driver.find_element_by_xpath('//*[@id="peers"]/div[1]/div[1]/p/a[2]').text

        info = {
            "name": name,
            "link": link,
            "bse": bse,
            "nse": nse,
            "about": about,
            "industry": industry,
            "sector": sector,
        }
        print(info)

    def nse(self):
        try:
            data = self.driver.find_element_by_xpath('//*[@id="top"]/div[2]/a[3]/span').text
            nse = data.replace("NSE :", '').strip()
        except NoSuchElementException:
            return ''
        return nse


def main():
    reporter = Reporter(BASE_URL)
    reporter.run()
    reporter.company_details()


if __name__ == '__main__':
    main()
