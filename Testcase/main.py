import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from Testcase import page
from Testcase.page import MainPage


class PythonOrgSearch(unittest.TestCase):
    def setUp(self):
        service = Service("/home/lukasz/chromedriver-linux64/chromedriver")
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("https://www.python.org")
        self.driver.maximize_window()

    def test_search_python(self):
        mainPage = page.MainPage(self.driver)
        assert mainPage.is_title_matches()
        mainPage.search_text_element = "pycon"
        mainPage.click_go_button()
        search_result_page = page.SearchResultPage(self.driver)
        assert search_result_page.is_results_found()



    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
