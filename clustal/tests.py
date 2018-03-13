from django.conf import settings
from django.test import SimpleTestCase, override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from os import path, mkdir
from subprocess import Popen, PIPE
from shutil import rmtree
from util.get_bin_name import get_bin_name
from celery.contrib.testing.worker import start_worker
from i5k.celery import app

DEBUG = False


@override_settings(DEBUG=True)
class ClustalLoadExampleTestCase(StaticLiveServerTestCase):
    def setUp(self):
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
        # Start up celery worker for testing
        self.celery_worker = start_worker(app)
        self.celery_worker.__enter__()

    def test(self):
        self.driver.get('%s%s' % (self.live_server_url, '/clustal/'))
        # wait at most 2 seconds to let page load, or timeout exception
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'txt')))
        self.driver.find_element_by_class_name('txt').click()
        self.driver.find_element_by_id('clustalo_submit').click()
        wait.until(EC.presence_of_element_located((By.ID, 'clustal-success')))

    def tearDown(self):
        self.driver.close()
        # Close worker for testing
        self.celery_worker.__exit__(None, None, None)


@override_settings(DEBUG=True)
class ClustalUploadFileTestCase(StaticLiveServerTestCase):
    def setUp(self):
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
        # Start up celery worker for testing
        self.celery_worker = start_worker(app)
        self.celery_worker.__enter__()

    def tearDown(self):
        self.driver.close()
        # Close worker for testing
        self.celery_worker.__exit__(None, None, None)

    def test(self):
        self.driver.get('%s%s' % (self.live_server_url, '/clustal/'))
        wait = WebDriverWait(self.driver, 10)
        example_file_path = path.join(settings.PROJECT_ROOT, 'example', 'blastdb', 'Cimex_sample_pep_query.faa')
        self.driver.find_element_by_name('query-file').send_keys(example_file_path)
        self.driver.find_element_by_xpath('//div//input[@value="Search"]').click()
        wait.until(EC.presence_of_element_located((By.ID, 'clustal-success')))


class ClustalBinaryTestCase(SimpleTestCase):
    def test_clustalo(self):
        test_dir = path.join(settings.PROJECT_ROOT, 'test_clustal')
        if not path.exists(test_dir):
            mkdir(test_dir)
        bin_name = get_bin_name()
        if bin_name == 'win32':
            return
        program_path = path.join(settings.PROJECT_ROOT, 'clustal', bin_name, 'clustalo')
        example_file_path = path.join(settings.PROJECT_ROOT, 'example', 'blastdb', 'Cimex_sample_pep_query.faa')
        out_file_path = path.join(test_dir, 'test.out')
        ph_file_path = path.join(test_dir, 'test.ph')
        args = [program_path, '--infile=' + example_file_path,
                '--outfile=' + out_file_path,
                '--guidetree-out=' + ph_file_path,
                '--full', '--full-iter', '--iterations=0',
                '--outfmt=clu', '--output-order=tree-order']
        try:
            p = Popen(args, stdin=PIPE, stdout=PIPE)
            p.wait()
            self.assertEqual(p.returncode, 0)
        finally:
            rmtree(test_dir)

    def test_clustalw(self):
        test_dir = path.join(settings.PROJECT_ROOT, 'test_clustal')
        if not path.exists(test_dir):
            mkdir(test_dir)
        bin_name = get_bin_name()
        if bin_name == 'bin_win' or bin_name == 'bin_mac':
            return
        program_path = path.join(settings.PROJECT_ROOT, 'clustal', bin_name, 'clustalw2')
        example_file_path = path.join(settings.PROJECT_ROOT, 'example', 'blastdb', 'Cimex_sample_pep_query.faa')
        out_file_path = path.join(test_dir, 'test.out')
        args = [program_path, '-infile=' + example_file_path,
                '-OUTFILE=' + out_file_path,
                '-type=protein']
        try:
            p = Popen(args, stdin=PIPE, stdout=PIPE)
            p.wait()
            self.assertEqual(p.returncode, 0)
        finally:
            rmtree(test_dir)
