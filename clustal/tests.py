from django.conf import settings
from django.test import LiveServerTestCase, override_settings
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from os import path

class ClustalLoadExampleTestCase(LiveServerTestCase):
    def setUp(self):
        settings.DEBUG = True
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1280x800')
        self.driver = webdriver.Chrome(chrome_options=options)
        # To use with header
        # self.driver = webdriver.Chrome()
        # Or use different webdriver
        # self.driver = webdriver.PhantomJS()
        # self.driver = webdriver.Firefox()
        # self.driver.set_window_size(1280, 800)

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test(self):
        self.driver.get('%s%s' % (self.live_server_url, '/clustal/'))
        wait = WebDriverWait(self.driver, 5)  # wait at most 2 seconds to let page load, or timeout exception
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'txt')))
        self.driver.find_element_by_class_name('txt').click()
        self.driver.find_element_by_id('clustalo_submit').click()
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))
        self.assertEqual(self.driver.find_element_by_tag_name('h2').text, 'CLUSTAL Success')

    def tearDown(self):
        self.driver.close()


class UploadFileTestCase(LiveServerTestCase):
    def setUp(self):
        settings.DEBUG = True
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1280x800')
        self.driver = webdriver.Chrome(chrome_options=options)
        # To use with header
        # self.driver = webdriver.Chrome()
        # Or use different webdriver
        # self.driver = webdriver.PhantomJS()
        # self.driver = webdriver.Firefox()
        # self.driver.set_window_size(1280, 800)

    def tearDown(self):
        self.driver.close()

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test(self):
        self.driver.get('%s%s' % (self.live_server_url, '/clustal/'))
        wait = WebDriverWait(self.driver, 10)
        example_file_path = path.join(settings.PROJECT_ROOT, 'example', 'blastdb', 'Cimex_sample_pep_query.faa')
        self.driver.find_element_by_name('query-file').send_keys(example_file_path)
        self.driver.find_element_by_xpath('//div//input[@value="Search"]').click()
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))
        self.assertEqual(self.driver.find_element_by_tag_name('h2').text, 'CLUSTAL Success')
