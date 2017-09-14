from django.test import SimpleTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class FrontEndTestCase(SimpleTestCase):
    
    @classmethod
    def setUpClass(self):
        super(FrontEndTestCase, self).setUpClass()
        self.driver = webdriver.Chrome()
        # Or used different webdriver
        # self.driver = webdriver.PhantomJS()
        # self.driver = webdriver.Firefox()
        self.driver.set_window_size(1024, 768)
        self.driver.get("http://127.0.0.1:8000/blast/test/")
        wait = WebDriverWait(self.driver, 2) # wait at most 2 seconds to let page load, or timeout exception
        wait.until(EC.element_to_be_clickable((By.ID, "athalia-rosae")))

    @classmethod
    def tearDownClass(self):
        super(FrontEndTestCase, self).tearDownClass()
        self.driver.close()

    def test_click_all_organism(self):
        # click the checkbox for all-organism
        self.driver.find_element_by_class_name("all-organism-checkbox").click()
        # Find all checkboxs of all organisms and check if they are all selected
        organism_checkboxs = self.driver.find_elements_by_class_name("organism-checkbox")
        for c in organism_checkboxs:
            self.assertEqual(c.is_selected() ,True)