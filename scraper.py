import csv
import os
import sys
from openpyxl import load_workbook
from selenium.common.exceptions import NoSuchElementException
import numpy as np
import re
import pandas as pd
from pandas import Series, ExcelWriter
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

    BASE_URL,
    WEB,
    HEADER
)


class Reporter:

    def __init__(self, base_url):
        self.base_url = base_url
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        set_browser_in_fullScreen(options)
        self.driver = get_chrome_web_driver(options)
        self.dfs = []

    def run(self):
        print("starting Script")
        self.driver.get(self.base_url)
        pause = random.randint(2, 5)
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
                """basic info"""
                bse = self.basic_info()

                table_name = "profit-loss"
                self.scroll_element(table_name)
                self.open_sales_expenses(5)
                data = self.parse_page()
                df = self.results(data[2])

                time.sleep(2)
                table_name = "balance-sheet"
                self.scroll_element(table_name)
                time.sleep(1)
                self.open_balance_sheet()
                time.sleep(1)
                data = self.parse_page()
                df1 = self.results(data[3])
                # table_name = "shareholding"
                # self.scroll_element(table_name)
                # self.open_shareholding()
                # time.sleep(2)
                # data = self.parse_page()
                # df2 = self.quarterly_results(data[6], bse)
                self.csvwrite(df, df1, bse, i=0)
                # self.write_shareholding(df2)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print("line->" + str(exc_tb.tb_lineno))
                print('Exception occurred in complete_details() method->' + str(e))
                self.driver.save_screenshot("lol.png")
                continue

    def csvwrite(self, n1, n2, num, i=None):
        filename = "finance.csv"
        if os.path.isfile(filename):
            result = pd.concat([n1, n2], axis=1)
            result['company_id'] = num
            self.dfs.append(result)
            frame = pd.concat(self.dfs, axis=0)
            df = pd.read_csv(filename)
            print("frame", frame)
            print("df", df)
            # if frame != df:
            i += 1
            frame.to_csv(filename, header=False, mode='a')
        else:
            self.check_file()
            result = pd.concat([n1, n2], axis=1)
            result['company_id'] = num
            self.dfs.append(result)
            frame = pd.concat(self.dfs, axis=0)

            i += 1
            frame.to_csv(filename, header=False, mode='a')

    def write_shareholding(self, df):
        file_name = "financial.xlsx"
        try:
            writer = pd.ExcelWriter(file_name, engine='openpyxl')
            print("writer", writer)
            if os.path.exists(file_name):
                print("yes")
                book = load_workbook(file_name)
                print(book)
                writer.book = book

            df.to_excel(writer, sheet_name="share")
            writer.save()
            writer.close()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("line->" + str(exc_tb.tb_lineno))
            print('Exception occurred in write_shareholding() method->' + str(e))

    def parse_page(self):
        page = self.driver.page_source
        soup = BeautifulSoup(page, "html.parser")
        data = soup.find_all("table", {"class": "data-table"})
        # print(data)
        return data

    def results(self, gdp):
        table1 = gdp
        body = table1.find_all("tr")
        head = body[0]
        # print(head)
        body_rows = body[1:]
        headings = []

        for item in head.find_all("th"):
            item = item.text.rstrip("\n")
            headings.append(item)
        all_rows = []
        # print("headings", headings)
        for row_num in range(len(body_rows)):
            row = []
            for row_item in body_rows[row_num].find_all("td"):
                aa = re.sub("(\xa0)|(\n)|,", "", row_item.text)
                row.append(aa.strip())
            all_rows.append(row)
        # print("allrow", all_rows)
        nest = {k[0]: k[1:] for k in all_rows}
        d = {k: dict(zip(headings[1:], v)) for k, v in nest.items()}
        df = pd.DataFrame(d)
        return df

    def append_to_csv(self, df, file):
        with open(file) as f:
            header = next(csv.reader(f))
        columns = df.columns
        for column in set(header) - set(columns):
            df[column] = ''
        df = df[header]
        df.to_csv(file, index=False, header=False, mode='a')

    def check_file(self):
        filename = 'finance.csv'
        with open(filename, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(HEADER)

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
        time.sleep(1)
        self.driver.find_element_by_xpath(
            f'//body[1]/main[1]/section[6]/div[2]/table[1]/tbody[1]/tr[1]/td[1]/button[1]').click()
        self.driver.find_element_by_xpath(
            f'//body[1]/main[1]/section[6]/div[2]/table[1]/tbody[1]/tr[4]/td[1]/button[1]').click()
        time.sleep(1)
        self.driver.find_elements_by_class_name("button-plain")[11].click()
        time.sleep(2)
        # self.driver.find_elements_by_class_name("button-plain")[12].click()
        self.driver.find_element_by_xpath("//*[contains(text(), 'Other Assets')]").click()
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
    header_added = False

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
            "company_id": bse,
            "name": name,
            "link": link,
            "bse": bse,
            "nse": nse,
            "industry": industry,
            "sector": sector,
            "about": about,

        }
        # print(info)
        file_name = 'company.csv'

        with open(file_name, "a") as f:
            w = csv.DictWriter(f, info.keys())
            if not self.header_added:
                w.writeheader()
                self.header_added = True
            w.writerow(info)
        # df = pd.DataFrame([info])
        # print("dgh", df)
        # df.to_csv("file2.csv", mode='a', index=False, header=False)
        return bse

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
