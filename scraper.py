import re
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
    BASE_URL
)


class Reporter:

    def __init__(self, base_url):
        # self.search_term = search_term
        self.base_url = base_url
        # self.currency = currency
        options = get_web_driver_options()
        # set_automation_as_head_less(options)
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
        # self.results_per_page()
        self.link()

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
        print(links)
        print(len(links))


def main():
    reporter = Reporter(BASE_URL)
    reporter.run()


if __name__ == '__main__':
    main()
