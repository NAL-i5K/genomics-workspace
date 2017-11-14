from os import path, remove
from shutil import copyfile
from django.test import LiveServerTestCase, override_settings
from django.conf import settings
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

display_name = 'test'
short_name = 'test'
title = 'clec_peptide_example_BLASTdb.fa'
test_files = [
    'clec_peptide_example_BLASTdb.fa',
]


class HmmerAdminTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(self):
        super(HmmerAdminTestCase, self).setUpClass()
        settings.DEBUG = True
        User = get_user_model()
        self.username = 'test'
        self.password = 'test'
        User.objects.create_superuser(
            username=self.username,
            password=self.password,
            email='test@test.com')
        # headless chrome driver
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

    @classmethod
    def tearDownClass(self):
        self.driver.close()
        super(HmmerAdminTestCase, self).tearDownClass()

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test(self):
        self.driver.get('%s%s' % (self.live_server_url, '/admin/'))
        # wait at most 5 seconds to let page load, or timeout exception
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.presence_of_element_located((By.ID, 'id_username')))
        username_input = self.driver.find_element_by_name('username')
        username_input.send_keys(self.username)
        password_input = self.driver.find_element_by_name('password')
        password_input.send_keys(self.password)
        self.driver.find_element_by_xpath('//input[@value="Log in"]').click()
        # add organism
        self.driver.get('%s%s' % (self.live_server_url, '/admin/app/organism/add/'))
        display_name_input = self.driver.find_element_by_id('id_display_name')
        short_name_input = self.driver.find_element_by_id('id_short_name')
        # TODO: check functionality of automatically fetching tax_id and
        # description
        # description_input = self.driver.find_element_by_id('id_description')
        # tax_id_input = self.driver.find_element_by_id('id_tax_id')
        display_name_input.send_keys(display_name)
        # check auto fill-in short name should be the same as display name
        self.assertEqual(short_name_input.get_attribute('value'), display_name)
        short_name_input.clear()
        short_name_input.send_keys(short_name)
        self.driver.find_element_by_name('_save').click()
        prepare_test_fasta_file()
        self.driver.get('%s%s' % (self.live_server_url, '/admin/hmmer/hmmerdb/add/'))
        dropdown = self.driver.find_element_by_css_selector('button[data-id=id_organism]')
        dropdown.click()
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, display_name)))
        fasta_file_input = self.driver.find_element_by_id('id_fasta_file')
        fasta_file_input.send_keys('/media/blast/db/clec_peptide_example_BLASTdb.fa')
        title_input = self.driver.find_element_by_id('id_title')
        title_input.clear()
        title_input.send_keys(title)
        self.driver.find_element_by_id('id_is_shown').click()
        self.driver.find_element_by_name('_save').click()
        self.driver.find_element_by_name('_save').click()
        query = (
            '>Sample_Query_CLEC000107-RA\n'
            'MFYFKNLTEKVIYVKKKKNENTIVMYTQNTRVVNNARREGVPITTQQKWGGGQNKQHFPVKNTAK'
            'LDQETEELKHKTIPLSLGKLIQKERMAKGWSQKEFATKCNEKPQVVNDYEAGRGIPNQAIIGKME'
            'RVLGKIRRNVTQAEGCRNYQSKNYSKSIQQ*'
        )
        send_query(query, self.driver, self.live_server_url)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))
        self.assertEqual(self.driver.find_element_by_tag_name('h2').text, 'HMMER Success')


def send_query(query, driver, live_server_url):
    driver.get('%s%s' % (live_server_url, '/hmmer/'))
    wait = WebDriverWait(driver, 10)
    organism_checkbox_xpath = '//input[@organism="' + display_name + '"]'
    wait.until(EC.element_to_be_clickable((By.XPATH, organism_checkbox_xpath)))
    element = driver.find_element_by_xpath(organism_checkbox_xpath)
    all_checkbox = driver.find_element_by_class_name('all-organism-checkbox')
    hover = ActionChains(driver).move_to_element(all_checkbox).move_to_element(element)
    hover.perform()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="' + title + '"]')))
    driver.find_element_by_xpath('//input[@value="' + title + '"]').click()
    driver.find_element_by_id('query-textarea').send_keys(query)
    driver.find_element_by_xpath('//div//input[@value="Search"]').click()


def prepare_test_fasta_file():
    for file in test_files:
        if path.exists(path.join(settings.PROJECT_ROOT, 'media', 'blast', 'db', file)):
            remove(path.join(settings.PROJECT_ROOT, 'media', 'blast', 'db', file))
    copyfile(path.join(settings.PROJECT_ROOT, 'example', 'blastdb', 'clec_peptide_example_BLASTdb.fa'), path.join(settings.PROJECT_ROOT, 'media', 'blast', 'db', 'clec_peptide_example_BLASTdb.fa'))
