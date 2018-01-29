from __future__ import absolute_import
from os import path, remove, chmod, mkdir, chdir
from shutil import rmtree
import stat as Perm
from subprocess import Popen, PIPE
from shutil import copyfile
from django.test import SimpleTestCase, LiveServerTestCase, override_settings
from django.conf import settings
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from hmmer.models import HmmerDB
from app.models import Organism
from filebrowser.base import FileObject
from hmmer.views import generate_hmmer_args
from util.get_bin_name import get_bin_name

DEBUG = False

tax_id = 79782
display_name = 'test'
short_name = 'test'
title = 'clec_peptide_example_BLASTdb.fa'
test_files = [
    'clec_peptide_example_BLASTdb.fa',
]
query = (
    '>Sample_Query_CLEC000107-RA\n'
    'MFYFKNLTEKVIYVKKKKNENTIVMYTQNTRVVNNARREGVPITTQQKWGGGQNKQHFPVKNTAK'
    'LDQETEELKHKTIPLSLGKLIQKERMAKGWSQKEFATKCNEKPQVVNDYEAGRGIPNQAIIGKME'
    'RVLGKIRRNVTQAEGCRNYQSKNYSKSIQQ*'
)


class HmmerAdminTestCase(LiveServerTestCase):
    def setUp(self):
        settings.DEBUG = True
        User = get_user_model()
        self.username = 'test'
        self.password = 'test'
        User.objects.create_superuser(
            username=self.username,
            password=self.password,
            email='test@test.com')
        if not DEBUG:
            # headless chrome driver
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1280x800')
            self.driver = webdriver.Chrome(chrome_options=options)
        else:
            # use with header
            self.driver = webdriver.Chrome()
            # Or use different webdriver
            # self.driver = webdriver.PhantomJS()
            # self.driver = webdriver.Firefox()
            self.driver.set_window_size(1280, 800)

    def tearDown(self):
        self.driver.close()

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


class LoadSeqExampleTestCase(LiveServerTestCase):
    def setUp(self):
        Organism.objects.create(
            display_name=display_name, short_name=short_name,
            tax_id=tax_id)
        organism = Organism.objects.get(short_name=short_name)
        prepare_test_fasta_file()
        self.files = test_files
        HmmerDB.objects.create(
            fasta_file=FileObject('/blast/db/clec_peptide_example_BLASTdb.fa'),
            organism=organism, is_shown=True, title=title)
        if not DEBUG:
            # headless chrome driver
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1280x800')
            self.driver = webdriver.Chrome(chrome_options=options)
        else:
            # use with header
            self.driver = webdriver.Chrome()
            # Or use different webdriver
            # self.driver = webdriver.PhantomJS()
            # self.driver = webdriver.Firefox()
            self.driver.set_window_size(1280, 800)

    def tearDown(self):
        self.driver.close()

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test(self):
        self.driver.get('%s%s' % (self.live_server_url, '/hmmer/'))
        wait = WebDriverWait(self.driver, 10)
        organism_checkbox_xpath = '//input[@organism="' + display_name + '"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, organism_checkbox_xpath)))
        element = self.driver.find_element_by_xpath(organism_checkbox_xpath)
        all_checkbox = self.driver.find_element_by_class_name('all-organism-checkbox')
        hover = ActionChains(self.driver).move_to_element(all_checkbox).move_to_element(element)
        hover.perform()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="' + title + '"]')))
        self.driver.find_element_by_xpath('//input[@value="' + title + '"]').click()
        self.driver.find_element_by_class_name('load-example-seq').click()
        self.driver.find_element_by_xpath('//div//input[@value="Search"]').click()
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))
        self.assertEqual(self.driver.find_element_by_tag_name('h2').text, 'HMMER Success')


class LoadAlignExampleTestCase(LiveServerTestCase):
    def setUp(self):
        Organism.objects.create(
            display_name=display_name, short_name=short_name,
            tax_id=tax_id)
        organism = Organism.objects.get(short_name=short_name)
        prepare_test_fasta_file()
        self.files = test_files
        HmmerDB.objects.create(
            fasta_file=FileObject('/blast/db/clec_peptide_example_BLASTdb.fa'),
            organism=organism, is_shown=True, title=title)
        if not DEBUG:
            # headless chrome driver
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1280x800')
            self.driver = webdriver.Chrome(chrome_options=options)
        else:
            # use with header
            self.driver = webdriver.Chrome()
            # Or use different webdriver
            # self.driver = webdriver.PhantomJS()
            # self.driver = webdriver.Firefox()
            self.driver.set_window_size(1280, 800)

    def tearDown(self):
        self.driver.close()

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test(self):
        self.driver.get('%s%s' % (self.live_server_url, '/hmmer/'))
        wait = WebDriverWait(self.driver, 10)
        organism_checkbox_xpath = '//input[@organism="' + display_name + '"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, organism_checkbox_xpath)))
        element = self.driver.find_element_by_xpath(organism_checkbox_xpath)
        all_checkbox = self.driver.find_element_by_class_name('all-organism-checkbox')
        hover = ActionChains(self.driver).move_to_element(all_checkbox).move_to_element(element)
        hover.perform()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="' + title + '"]')))
        self.driver.find_element_by_xpath('//input[@value="' + title + '"]').click()
        self.driver.find_element_by_class_name('load-example-aln').click()
        self.driver.find_element_by_xpath('//div//input[@value="Search"]').click()
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))
        self.assertEqual(self.driver.find_element_by_tag_name('h2').text, 'HMMER Success')


class UploadFileTestCase(LiveServerTestCase):
    def setUp(self):
        settings.DEBUG = True
        Organism.objects.create(
            display_name=display_name, short_name=short_name,
            tax_id=tax_id)
        organism = Organism.objects.get(short_name=short_name)
        prepare_test_fasta_file()
        self.files = test_files
        HmmerDB.objects.create(
            fasta_file=FileObject('/blast/db/clec_peptide_example_BLASTdb.fa'),
            organism=organism, is_shown=True, title=title)
        if not DEBUG:
            # headless chrome driver
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1280x800')
            self.driver = webdriver.Chrome(chrome_options=options)
        else:
            # use with header
            self.driver = webdriver.Chrome()
            # Or use different webdriver
            # self.driver = webdriver.PhantomJS()
            # self.driver = webdriver.Firefox()
            self.driver.set_window_size(1280, 800)

    def tearDown(self):
        self.driver.close()

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test(self):
        self.driver.get('%s%s' % (self.live_server_url, '/hmmer/'))
        wait = WebDriverWait(self.driver, 10)
        organism_checkbox_xpath = '//input[@organism="' + display_name + '"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, organism_checkbox_xpath)))
        element = self.driver.find_element_by_xpath(organism_checkbox_xpath)
        all_checkbox = self.driver.find_element_by_class_name('all-organism-checkbox')
        hover = ActionChains(self.driver).move_to_element(all_checkbox).move_to_element(element)
        hover.perform()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="' + title + '"]')))
        self.driver.find_element_by_xpath('//input[@value="' + title + '"]').click()
        example_file_path = path.join(settings.PROJECT_ROOT, 'example', 'blastdb', 'Cimex_sample_pep_query.faa')
        self.driver.find_element_by_name('query-file').send_keys(example_file_path)
        self.driver.find_element_by_xpath('//div//input[@value="Search"]').click()
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))
        self.assertEqual(self.driver.find_element_by_tag_name('h2').text, 'HMMER Success')


class HmmerViewFunctionTestCase(SimpleTestCase):
    def test_generate_hmmer_args(self):
        args = generate_hmmer_args('phmmer', '/test/hmmer/bin_mac',
                                   '/test/hmmer/task/123/test123.in',
                                   ['--incE', u'0.01', '--incdomE', u'0.03',
                                    '-E', u'0.01', '--domE', u'0.03'],
                                   ['/test/test.fa'])
        self.assertEqual(args,
                         [['/test/hmmer/bin_mac/phmmer', '-o',
                           '0.out', '--incE', u'0.01', '--incdomE', u'0.03',
                           '-E', u'0.01', '--domE', u'0.03',
                           '/test/hmmer/task/123/test123.in', '/test/test.fa']])


class HmmerBinaryTestCase(SimpleTestCase):
    def test_phmmer(self):
        run_hmmer('phmmer', self.assertEqual)

    def test_hmmsearch(self):
        run_hmmer('hmmsearch', self.assertEqual)


def run_hmmer(program, assertEqual):
    test_dir = path.join(settings.PROJECT_ROOT, 'test_hmmer')
    if not path.exists(test_dir):
        mkdir(test_dir)
    chmod(test_dir, Perm.S_IRWXU | Perm.S_IRWXG | Perm.S_IRWXO)
    if program == 'phmmer':
        input_file_dir = path.join(settings.PROJECT_ROOT, 'example', 'blastdb')
        query_filename = path.join(test_dir, 'Cimex_sample_pep_query.faa')
        copyfile(path.join(input_file_dir, 'Cimex_sample_pep_query.faa'), query_filename)
    else:  # program == 'hmmersearch'
        input_file_dir = path.join(settings.PROJECT_ROOT, 'example', 'hmmer')
        query_filename = path.join(test_dir, 'example.MSA')
        copyfile(path.join(input_file_dir, 'example.MSA'), query_filename)
    db_file = path.join(test_dir, 'AGLA_new_ids.faa')
    copyfile(path.join(settings.PROJECT_ROOT, 'example', 'blastdb', 'AGLA_new_ids.faa'), db_file)
    chmod(query_filename,
          Perm.S_IRWXU | Perm.S_IRWXG | Perm.S_IRWXO)
    chmod(db_file,
          Perm.S_IRWXU | Perm.S_IRWXG | Perm.S_IRWXO)
    bin_name = get_bin_name()
    if bin_name == 'bin_win':
        return
    program_path = path.join(settings.PROJECT_ROOT, 'hmmer', bin_name)
    option_params = ['--incE', u'0.01', '--incdomE', u'0.03', '-E', u'0.01', '--domE', u'0.03']
    db_list = [db_file]
    args = generate_hmmer_args(program, program_path, query_filename, option_params, db_list)
    chdir(test_dir)
    try:
        run_commands(args, assertEqual)
    finally:
        rmtree(test_dir)


def run_commands(args_list, assertEqual):
    for args in args_list:
        p = Popen(args, stdin=PIPE, stdout=PIPE)
        p.wait()
        assertEqual(p.returncode, 0)
