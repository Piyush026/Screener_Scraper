import sys

import pandas as pd
import random
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import InvalidSessionIdException
from scraper import Reporter
from scraper_config import (
    get_web_driver_options,
    get_chrome_web_driver,
    set_browser_as_incognito,
    set_ignore_certificate_error,
    set_browser_in_fullScreen,
    set_automation_as_head_less,
    USERNAME,
    PASSWORD,
    user, user1, user2, user3, user4, user5, user6,

    BASE_URL,
    WEB

)


class Report:

    def __init__(self, base_url):
        self.base_url = base_url
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        set_browser_in_fullScreen(options)
        # set_automation_as_head_less
        self.driver = get_chrome_web_driver(options)
        self.dfs = []
        self.final = []

    def run(self):
        print("starting Script")
        self.driver.get(self.base_url)
        pause = random.randint(2, 5)
        print(f"Sleeping for {pause}...")
        time.sleep(pause)
        self.login(user1, PASSWORD)

    def login(self, user, password):
        print("start login")
        self.driver.find_element_by_xpath("/html/body/nav/div[1]/div/div[1]/div[3]/div[2]/a[1]").click()
        self.driver.find_element_by_xpath('//*[@id="id_username"]').send_keys(user)
        self.driver.find_element_by_xpath('//*[@id="id_password"]').send_keys(password)
        self.driver.find_element_by_xpath('/html/body/main/div/div/div[2]/form/button').click()
        self.create_links()
        flat_1 = [x for l in self.dfs for x in l]
        n = 500
        self.final = [flat_1[i:i + n] for i in range(0, len(flat_1), n)]
        self.csv(flat_1)
        # print(flat_1)

    def csv(self, num):

        df = pd.DataFrame(num, columns=['company'])
        df.to_csv('comp.csv', index=False)

    def create_links(self):
        for num in range(1, 39):
            try:
                url = f"https://www.screener.in/screen/raw/?sort=&order=&source=&query=Sales+%3E+-10000000000&limit=100&page={num}"
                self.driver.get(url)
                self.company_links = self.link()
                self.creating_linkssss()
                time.sleep(1)
            except InvalidSessionIdException:
                continue

    def close(self):
        self.driver.close()

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

    def creating_linkssss(self):

        new_list = [WEB + x for x in self.company_links]
        self.dfs.append(new_list)


def main():
    try:
        reporter = Report(BASE_URL)
        reporter.run()
        name = reporter.final
        print(name[2])
        for x in range(len(name)):
            try:
                # if x == 1:
                #     filename = f"finance{x}.csv"
                #     repo = Reporter(BASE_URL)
                #     repo.run(user, PASSWORD)
                #     repo.company_details(name[x], filename)
                if x == 2:
                    filename = f"finance{x}.csv"
                    repo1 = Reporter(BASE_URL)
                    repo1.run(user1, PASSWORD)
                    repo1.company_details(name[x], filename)
                # if x == 3:
                #     filename = f"finance{x}.csv"
                #     repo1 = Reporter(BASE_URL)
                #     repo1.run(user2, PASSWORD)
                #     repo1.company_details(name[x], filename)
                # if x == 4:
                #     filename = f"finance{x}.csv"
                #     repo1 = Reporter(BASE_URL)
                #     repo1.run(user3, PASSWORD)
                #     repo1.company_details(name[x], filename)
                # if x == 5:
                #     filename = f"finance{x}.csv"
                #     repo1 = Reporter(BASE_URL)
                #     repo1.run(user4, PASSWORD)
                #     repo1.company_details(name[x], filename)
                # if x == 6:
                #     filename = f"finance{x}.csv"
                #     repo1 = Reporter(BASE_URL)
                #     repo1.run(user5, PASSWORD)
                #     repo1.company_details(name[x], filename)
                # if x == 7:
                #     filename = f"finance{x}.csv"
                #     repo1 = Reporter(BASE_URL)
                #     repo1.run(user6, PASSWORD)
                #     repo1.company_details(name[x], filename)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print("line->" + str(exc_tb.tb_lineno))
                print('Exception occurred in main() method->' + str(e))
            #     continue
            # finally:
            #     reporter.close()

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("line->" + str(exc_tb.tb_lineno))
        print(str(e))


if __name__ == '__main__':
    main()
