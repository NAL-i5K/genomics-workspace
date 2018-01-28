from __future__ import print_function
from os import path, makedirs, remove
from shutil import copyfile, rmtree
from subprocess import Popen, PIPE
from django.conf import settings
from django.test import SimpleTestCase, TestCase, LiveServerTestCase, override_settings
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from filebrowser.base import FileObject
from blast.models import SequenceType, BlastDb, Sequence, JbrowseSetting
from app.models import Organism
from util.get_bin_name import get_bin_name

DEBUG = False

display_name = 'test'
short_name = 'test'
tax_id = 79782
dataset_type = 'abc'
title = 'clec_peptide_example_BLASTdb.fa'
test_files = [
    'clec_peptide_example_BLASTdb.fa',
    'clec_peptide_example_BLASTdb.fa.pog',
    'clec_peptide_example_BLASTdb.fa.phd',
    'clec_peptide_example_BLASTdb.fa.psd',
    'clec_peptide_example_BLASTdb.fa.phi',
    'clec_peptide_example_BLASTdb.fa.psi',
    'clec_peptide_example_BLASTdb.fa.phr',
    'clec_peptide_example_BLASTdb.fa.psq',
    'clec_peptide_example_BLASTdb.fa.pin',
]

peptide_seq = (">CLEC010822-PA:polypeptide ,Heat shock protein 70-2\\n"
        "MILHFLVLLFASALAADEKNKDVGTVVGIDLGTTYSCVGVYKNGRVEIIANDQGNRITPSYVAFTSEGERLIGDAAKNQLTTNPENTVFDAKRLIGREWTDSTVQDDIKFFPFKVLEKNSKPHIQVSTSQGNKMFAPEEISAMVLGKMKETAEAYLGKKVTHAVVTVPAYFNDAQRQATKDAGTISGLNVMRIINEPTAAAIAYGLDKKEGEKNVLVFDLGGGTFDVSLLTIDNGVFEVVSTNGDTHLGGEDFDQRVMDHFIKLYKKKKGKDIRKDNRAVQKLRREVEKAKRALSSSHQVRIEIESFYDGEDFSETLTRAKFEELNMDLFRSTMKPVQKVLEDADMNKKDVDEIVLVGGSTRIPKVQALVKEFFNGKEPSRGINPDEAVAYGAAVQAGVLSGEQDTDSIVLLDVNPLTLGIETVGGVMTKLIPRNTVIPTKKSQIFSTASDNQHTVTIQVYEGERPMTKDNHLLGKFDLTGIPPAPRGVPQIEVTFEIDANGILQVSAEDKGTGNREKIVITNDQNRLTPDDIDRMIKDAEKFADDDKKLKERVEARNELESYAYSLKNQLADKDKFGSKVTDSDKAKMEKAIEEKIKWLDENQDADSEAFKKQKKELEDVVQPIISKLYQGGAPPPPGAGPQSEDDLKDEL*\\n"
        ">OFAS004830-PA:polypeptide ,Heat shock protein 70-2\\n"
        "MAAGGSRPTRPAVGIDLGTTYSCVGYFDKGRVEIIANDQGNRVTPSYVAFTETDRIVGDAARGQAIMNPSNTVYDAKRLIGRKFDDPSVQADRKMWPFKVASKEGKPMIEVTYKGETRQFFPEEISSMVLSKMRETAESYIGKKVSNAVVTVPAYFNDSQRQATKDSGTIAGLNVLRIINEPTAAAVAYGLDKKGSGEINVLIFDLGGGTFDVSVLTIADGLFEVKATAGDTHLGGADFDNRMVQYFLEEFKRKTKKEVNDNKRALRRLQAACERAKRVLSTATQATVEIDSFVDGIDLYSAVSRAKFEEINSDLFRGTLGPVEKAIRDSKIPKNRIDEIVLVGGSTRIPKIQSLLVEYFNGKELNKTINPDEAVAYGAAVQAAIIVGDTSDEVKDVLLLDVTPLSLGIETAGGIMTNLIPRNTTIPVKHSQIFSTYSDNQPGVLIQVYEGERAMTKDNNLLGTFELRGFPPAPRGVPQIEVAFDVDANGILNVTAQEMSTKKTSKITITNDKGRLTKAQIEKMVKEAERYKSEDTAARETAEAKNGLESYCYAMKNSVEEAANLGRVTEDEMKSVVRKCNETIMWIEANRSATKMEFEKKMRETESVCKPIATKILSRGTQQNNAGGGTPTNERGPVIEEAD\\n"
        ">OFAS004738-PA:polypeptide ,Heat shock protein 70-1\\n"
        "MPAIGIDLGTTYSCVGVWQHGKVEIIANDQGNRTTPSYVAFSDTERLIGDAAKNQVAMNPQNTVFDAKRLIGRKYDDPKIQDDLKHWPFRVVDCSSKPKIQVEYKGETKTFAPEEISSMVLVKMKETAEAYLGGTVRDAVITVPAYFNDSQRQATKDAGAIAGLNVLRIINEPTAAALAYGLDKNLKGERNVLIFDLGGGTFDGPREQDHSLKGERNVLIFDLGGGTFDVSILTIDEGSLFEVKSTAGDTHLGGEDFDNRLVNHLAEEFKRKYRKDLKTNPRALRRLRTAAERAKRTLSSSTEASIEIDALFEGVDFYTKITRARFEELCSDLFRSTLQPVEKALQDAKLDKGLIHDVVLVGGSTRIPKIQNLLQNFFNGKSLNMSINPDEAVAYGAAVQAAILSGDQSSKIQDVLLVDVAPLSLGIETAGGVMTKIIERNTRI"
)

nucleotide_seq = (
    ">Scaffold1\\n"
    "GAAAAGTTAATTGTAAACTTTAATAAATAAATATTTTTTTAAAAACGAGTGTCGTTAAGACAAATTTATAACTTATATATATATAATTTGTTGAAGCCCTGAGAAGCGGTCAAGAGTGAGGTAATTTAGAAAAACGCATTTTTATTTGTTTGCCCGCGTTTCGACCTTTATTCGGGTCATCTTCAGGGCGTGGGTAAATAAGAAATGGCACCGCAAGAATAGCACCACACTTTATGTAAGTATAAAATACTTGGTTCAAAGTTCATATTTATATCTGTATTGCATTTTTTCAAATCAACATGTTTTGTAATTTACCCAGGCCCCGAAGATGACCCGGATAAAGGTCGAAACGCTGGCAAAACAAGAAAAATTGTGTTTTTCTAAAATGCCTCATTCTTCACCGCTCCTCTCGACTTCAAGAAATAATAAAATTATTTCATTTTACCATCA"
)


class FrontEndTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(self):
        super(FrontEndTestCase, self).setUpClass()
        settings.DEBUG = True
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

    @classmethod
    def tearDownClass(self):
        self.driver.close()
        super(FrontEndTestCase, self).tearDownClass()


class ClickAllTestCase(FrontEndTestCase):
    def test(self):
        self.driver.get('%s%s' % (self.live_server_url, '/blast/test/'))
        wait = WebDriverWait(self.driver, 2)  # wait at most 2 seconds to let page load, or timeout exception
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "all-organism-checkbox")))
        # click the checkbox for all-organism
        all_checkbox = self.driver.find_element_by_class_name("all-organism-checkbox")
        all_checkbox.click()
        # Find all checkboxs of all organisms and check if they are all selected
        organism_checkboxs = self.driver.find_elements_by_class_name("organism-checkbox")
        for c in organism_checkboxs:
            self.assertEqual(c.is_selected(), True)
        self.assertEqual(
            self.driver.find_element_by_css_selector("input.all-dataset-checkbox.nucleotide.genome-assembly").is_selected(),
            True)
        self.assertEqual(
            bool(self.driver.find_element_by_css_selector("input.all-dataset-checkbox.peptide.protein").get_attribute("disabled")),
            True)
        # unselect the checkbox for all-organism
        all_checkbox.click()
        for c in organism_checkboxs:
            self.assertEqual(c.is_selected(), False)
        self.assertEqual(
            self.driver.find_element_by_css_selector("input.all-dataset-checkbox.nucleotide.genome-assembly").is_selected(),
            False)
        self.assertEqual(
            bool(self.driver.find_element_by_css_selector("input.all-dataset-checkbox.peptide.protein").get_attribute("disabled")),
            False)


class NucleotideSequenceSimpleTestCase(FrontEndTestCase):
    def test(self):
        self.driver.get('%s%s' % (self.live_server_url, '/blast/test/'))
        # wait at most 2 seconds to let page load, or timeout exception
        wait = WebDriverWait(self.driver, 2)
        wait.until(EC.element_to_be_clickable((By.ID, "query-textarea")))
        # Insert sample nucleotide into textarea
        # Don't use send_keys(peptide_seq), since it's too slow
        self.driver.execute_script(
            "$('#query-textarea').val(\"" + nucleotide_seq
            + "\").keyup();")
        checkProgramOptions(
            self.driver, self.assertEqual,
            selected=[True, False, False, False, False],
            disabled=[False, True, False, True, False])
        reset_button = self.driver.find_element_by_css_selector("input.btn_reset")
        reset_button.click()
        checkProgramOptions(
            self.driver, self.assertEqual,
            selected=[True, False, False, False, False],
            disabled=[False, False, False, False, False])


class NucleotideSequenceComplexTestCase(FrontEndTestCase):
    def test(self):
        self.driver.get('%s%s' % (self.live_server_url, '/blast/test/'))
        # wait at most 2 seconds to let page load, or timeout exception
        wait = WebDriverWait(self.driver, 2)
        wait.until(EC.element_to_be_clickable((By.ID, "query-textarea")))
        # Insert sample nucleotide into textarea
        # Don't use send_keys(peptide_seq), since it's too slow
        self.driver.execute_script(
            "$('#query-textarea').val(\"" + nucleotide_seq
            + "\").keyup(); $('#query-textarea').val('').keyup();")
        checkProgramOptions(
            self.driver, self.assertEqual,
            selected=[True, False, False, False, False],
            disabled=[False, False, False, False, False])


class PeptideSequenceSimpleTestCase(FrontEndTestCase):
    def test(self):
        self.driver.get('%s%s' % (self.live_server_url, '/blast/test/'))
        # wait at most 2 seconds to let page load, or timeout exception
        wait = WebDriverWait(self.driver, 2)
        wait.until(EC.element_to_be_clickable((By.ID, "query-textarea")))
        # Insert sample peptide into textarea
        # Don't use send_keys(peptide_seq), since it's too slow
        self.driver.execute_script("$('#query-textarea').val('" + peptide_seq + "').keyup();")
        checkProgramOptions(
            self.driver, self.assertEqual,
            selected=[False, True, False, False, False],
            disabled=[True, False, True, False, True])
        reset_button = self.driver.find_element_by_css_selector("input.btn_reset")
        reset_button.click()
        checkProgramOptions(
            self.driver, self.assertEqual,
            selected=[True, False, False, False, False],
            disabled=[False, False, False, False, False])


class PeptideSequenceComplexTestCase(FrontEndTestCase):
    def test(self):
        self.driver.get('%s%s' % (self.live_server_url, '/blast/test/'))
        # wait at most 2 seconds to let page load, or timeout exception
        wait = WebDriverWait(self.driver, 2)
        wait.until(EC.element_to_be_clickable((By.ID, "query-textarea")))
        # Insert sample peptide into textarea
        # Don't use send_keys(peptide_seq), since it's too slow
        self.driver.execute_script("$('#query-textarea').val('" + peptide_seq + "').keyup(); $('#query-textarea').val('').keyup();")
        checkProgramOptions(self.driver, self.assertEqual, selected=[True, False, False, False, False], disabled=[False, False, False, False, False])


class LoadExampleNucleotideSequenceTestCase(FrontEndTestCase):
    def test(self):
        self.driver.get('%s%s' % (self.live_server_url, '/blast/test/'))
        # wait at most 2 seconds to let page load, or timeout exception
        wait = WebDriverWait(self.driver, 2)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.load-nucleotide.txt")))
        self.driver.find_element_by_css_selector("span.load-nucleotide.txt").click()
        checkProgramOptions(self.driver, self.assertEqual, selected=[True, False, False, False, False], disabled=[False, True, False, True, False])


class LoadExamplePeptideSequenceTestCase(FrontEndTestCase):
    def test(self):
        self.driver.get('%s%s' % (self.live_server_url, '/blast/test/'))
        wait = WebDriverWait(self.driver, 2) # wait at most 2 seconds to let page load, or timeout exception
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.load-peptide.txt")))
        self.driver.find_element_by_css_selector("span.load-peptide.txt").click()
        checkProgramOptions(self.driver, self.assertEqual, selected=[False, True, False, False, False], disabled=[True, False, True, False, True])


class ClickSequenceTypeTestCase(FrontEndTestCase):
    def test(self):
        self.driver.get('%s%s' % (self.live_server_url, '/blast/test/'))
        # wait at most 2 seconds to let page load, or timeout exception
        wait = WebDriverWait(self.driver, 2)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.all-dataset-checkbox.nucleotide.genome-assembly")))
        assembly = self.driver.find_element_by_css_selector("input.all-dataset-checkbox.nucleotide.genome-assembly")
        transcript = self.driver.find_element_by_css_selector("input.all-dataset-checkbox.nucleotide.transcript")
        protein = self.driver.find_element_by_css_selector("input.all-dataset-checkbox.protein.peptide")
        checkSeqenceTypes(self.driver, self.assertEqual, selected=[False, False, False], disabled=[False, False, False])
        # select assembly
        assembly.click()
        checkSeqenceTypes(self.driver, self.assertEqual, selected=[True, False, False], disabled=[False, False, True])
        checkProgramOptions(self.driver, self.assertEqual, selected=[True, False, False, False, False], disabled=[False, False, False, True, True])
        # unselect assembly
        assembly.click()
        checkSeqenceTypes(self.driver, self.assertEqual, selected=[False, False, False], disabled=[False, False, False])
        checkProgramOptions(self.driver, self.assertEqual, selected=[True, False, False, False, False], disabled=[False, False, False, False, False])
        # select transcript
        transcript.click()
        checkSeqenceTypes(self.driver, self.assertEqual, selected=[False, True, False], disabled=[False, False, True])
        checkProgramOptions(self.driver, self.assertEqual, selected=[True, False, False, False, False], disabled=[False, False, False, True, True])
        # unselect transcript
        transcript.click()
        checkSeqenceTypes(self.driver, self.assertEqual, selected=[False, False, False], disabled=[False, False, False])
        checkProgramOptions(self.driver, self.assertEqual, selected=[True, False, False, False, False], disabled=[False, False, False, False, False])
        # select protein
        protein.click()
        checkSeqenceTypes(self.driver, self.assertEqual, selected=[False, False, True], disabled=[True, True, False])
        checkProgramOptions(self.driver, self.assertEqual, selected=[False, False, False, True, False], disabled=[True, True, True, False, False])
        # unselect protein
        protein.click()
        checkSeqenceTypes(self.driver, self.assertEqual, selected=[False, False, False], disabled=[False, False, False])
        checkProgramOptions(self.driver, self.assertEqual, selected=[True, False, False, False, False], disabled=[False, False, False, False, False])


class HoverIntentTestCase(FrontEndTestCase):
    def test(self):
        self.driver.get('%s%s' % (self.live_server_url, '/blast/test/'))
        # wait at most 2 seconds to let page load, or timeout exception
        wait = WebDriverWait(self.driver, 2)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "all-organism-checkbox")))
        all_checkbox = self.driver.find_element_by_class_name("all-organism-checkbox")
        element = self.driver.find_element_by_id("anoplophora-glabripennis")
        hover = ActionChains(self.driver).move_to_element(all_checkbox).move_to_element(element)
        hover.perform()
        self.assertEqual(self.driver.find_element_by_id("Agla_Btl03082013.genome_new_ids.fa").is_displayed(), False)
        WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located((By.ID, "Agla_Btl03082013.genome_new_ids.fa")))
        self.assertEqual(self.driver.find_element_by_id("Agla_Btl03082013.genome_new_ids.fa").is_displayed(), True)


def checkProgramOptions(driver, assertEqual, selected=[True, False, False, False, False], disabled=[False, False, False, False, False]):
    blastn_radio = driver.find_element_by_css_selector("input.program.blastn")
    tblastn_radio = driver.find_element_by_css_selector("input.program.tblastn")
    tblastx_radio = driver.find_element_by_css_selector("input.program.tblastx")
    blastp_radio = driver.find_element_by_css_selector("input.program.blastp")
    blastx_radio = driver.find_element_by_css_selector("input.program.blastx")
    # check if selected
    assertEqual(blastn_radio.is_selected(), selected[0])
    assertEqual(tblastn_radio.is_selected(), selected[1])
    assertEqual(tblastx_radio.is_selected(), selected[2])
    assertEqual(blastp_radio.is_selected(), selected[3])
    assertEqual(blastx_radio.is_selected(), selected[4])
    # check if disabled
    assertEqual(bool(blastn_radio.get_attribute("disabled")), disabled[0])
    assertEqual(bool(tblastn_radio.get_attribute("disabled")), disabled[1])
    assertEqual(bool(tblastx_radio.get_attribute("disabled")), disabled[2])
    assertEqual(bool(blastp_radio.get_attribute("disabled")), disabled[3])
    assertEqual(bool(blastx_radio.get_attribute("disabled")), disabled[4])


def checkSeqenceTypes(driver, assertEqual, selected=[False, False, False],
                      disabled=[False, False, False]):
    assembly = driver.find_element_by_css_selector(
        "input.all-dataset-checkbox.nucleotide.genome-assembly")
    transcript = driver.find_element_by_css_selector(
        "input.all-dataset-checkbox.nucleotide.transcript")
    protein = driver.find_element_by_css_selector(
        "input.all-dataset-checkbox.protein.peptide")
    # check if selected
    assertEqual(assembly.is_selected(), selected[0])
    assertEqual(transcript.is_selected(), selected[1])
    assertEqual(protein.is_selected(), selected[2])
    # check if disabled
    assertEqual(bool(assembly.get_attribute("disabled")), disabled[0])
    assertEqual(bool(transcript.get_attribute("disabled")), disabled[1])
    assertEqual(bool(protein.get_attribute("disabled")), disabled[2])


class BlastModelActionTestCase(TestCase):
    def setUp(self):
        Organism.objects.create(
            display_name=display_name, short_name=short_name,
            tax_id=tax_id)
        organism = Organism.objects.get(short_name=short_name)
        sequence = SequenceType.objects.create(
            molecule_type='prot', dataset_type=dataset_type)
        prepare_test_fasta_file()
        self.files = test_files
        BlastDb.objects.create(
            fasta_file=FileObject('/blast/db/clec_peptide_example_BLASTdb.fa'),
            organism=organism, type=sequence, is_shown=False, title=title)

    def test_makeblastdb(self):
        organism = Organism.objects.get(short_name=short_name)
        blastdb = BlastDb.objects.get(organism=organism)
        returncode, error, output = blastdb.makeblastdb()
        self.assertEqual(returncode, 0)
        self.assertEqual(error, '')
        for file in self.files:
            self.assertEqual(
                path.exists(path.join(settings.PROJECT_ROOT, 'media', 'blast', 'db', file)),
                True)

    def test_index_fasta(self):
        organism = Organism.objects.get(short_name=short_name)
        blastdb = BlastDb.objects.get(organism=organism)
        returncode, error, output = blastdb.index_fasta()
        self.assertEqual(returncode, 0)
        self.assertEqual(error, '')
        self.assertEqual(blastdb.title, title)
        all_sequence = Sequence.objects.all()
        self.assertEqual(len(all_sequence), 395)
        for s in all_sequence:
            self.assertEqual(s.blast_db.title, title)


class BlastAdminTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(self):
        super(BlastAdminTestCase, self).setUpClass()
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

    @classmethod
    def tearDownClass(self):
        self.driver.close()
        super(BlastAdminTestCase, self).tearDownClass()

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
        # add sequence type
        self.driver.get('%s%s' % (self.live_server_url, '/admin/blast/sequencetype/add/'))
        dropdown = self.driver.find_element_by_css_selector('button[data-id=id_molecule_type]')
        dropdown.click()
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Peptide')))
        option = self.driver.find_element_by_link_text('Peptide')
        option.click()
        dataset_type_input = self.driver.find_element_by_id('id_dataset_type')
        dataset_type_input.send_keys(dataset_type)
        self.driver.find_element_by_name('_save').click()
        # add blastdb
        prepare_test_fasta_file()
        self.driver.get('%s%s' % (self.live_server_url, '/admin/blast/blastdb/add/'))
        dropdown = self.driver.find_element_by_css_selector('button[data-id=id_organism]')
        dropdown.click()
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, display_name)))
        option = self.driver.find_element_by_link_text(display_name)
        option.click()
        dropdown = self.driver.find_element_by_css_selector('button[data-id=id_type]')
        dropdown.click()
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Peptide - ' + dataset_type )))
        option = self.driver.find_element_by_link_text('Peptide - ' + dataset_type)
        option.click()
        fasta_file_input = self.driver.find_element_by_id('id_fasta_file')
        fasta_file_input.send_keys('/media/blast/db/clec_peptide_example_BLASTdb.fa')
        title_input = self.driver.find_element_by_id('id_title')
        title_input.clear()
        title_input.send_keys(title)
        self.driver.find_element_by_name('_save').click()
        self.assertEqual(self.driver.find_element_by_css_selector('td.field-fasta_file_exists > img').get_attribute('alt'), 'true')
        self.assertEqual(self.driver.find_element_by_css_selector('td.field-blast_db_files_exists > img').get_attribute('alt'), 'false')
        self.assertEqual(self.driver.find_element_by_css_selector('td.field-sequence_set_exists > img').get_attribute('alt'), 'false')
        self.driver.find_element_by_id('action-toggle').click()
        dropdown = self.driver.find_element_by_xpath('//div[@class="actions"]//label//div//button[@data-toggle="dropdown"]')
        dropdown.click()
        option = self.driver.find_element_by_link_text('Run makeblastdb on selected entries, replaces existing files')
        option.click()
        self.driver.find_element_by_name('index').click()
        self.assertEqual(self.driver.find_element_by_css_selector('td.field-fasta_file_exists > img').get_attribute('alt'), 'true')
        self.assertEqual(self.driver.find_element_by_css_selector('td.field-blast_db_files_exists > img').get_attribute('alt'), 'true')
        self.assertEqual(self.driver.find_element_by_css_selector('td.field-sequence_set_exists > img').get_attribute('alt'), 'false')
        self.driver.find_element_by_id('action-toggle').click()
        dropdown = self.driver.find_element_by_xpath('//div[@class="actions"]//label//div//button[@data-toggle="dropdown"]')
        dropdown.click()
        option = self.driver.find_element_by_link_text('Populate Sequences table, replaces existing Sequence entries')
        option.click()
        self.driver.find_element_by_name('index').click()
        self.assertEqual(self.driver.find_element_by_css_selector('td.field-fasta_file_exists > img').get_attribute('alt'), 'true')
        self.assertEqual(self.driver.find_element_by_css_selector('td.field-blast_db_files_exists > img').get_attribute('alt'), 'true')
        self.assertEqual(self.driver.find_element_by_css_selector('td.field-sequence_set_exists > img').get_attribute('alt'), 'true')
        self.driver.find_element_by_id('id_form-0-is_shown').click()
        self.driver.find_element_by_name('_save').click()
        # test valid query
        query = (
            '>Sample_Query_CLEC000107-RA\n'
            'MFYFKNLTEKVIYVKKKKNENTIVMYTQNTRVVNNARREGVPITTQQKWGGGQNKQHFPVKNTAK'
            'LDQETEELKHKTIPLSLGKLIQKERMAKGWSQKEFATKCNEKPQVVNDYEAGRGIPNQAIIGKME'
            'RVLGKIRRNVTQAEGCRNYQSKNYSKSIQQ*'
        )
        send_query(query, self.driver, self.live_server_url)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'query-canvas-name')))


def prepare_test_fasta_file():
    for file in test_files:
        if path.exists(path.join(settings.PROJECT_ROOT, 'media', 'blast', 'db', file)):
            remove(path.join(settings.PROJECT_ROOT, 'media', 'blast', 'db', file))
    copyfile(path.join(settings.PROJECT_ROOT, 'example', 'blastdb', 'clec_peptide_example_BLASTdb.fa'), path.join(settings.PROJECT_ROOT, 'media', 'blast', 'db', 'clec_peptide_example_BLASTdb.fa'))


class BlastBinaryTestCase(SimpleTestCase):
    def test_blastp(self):
        run_blast('blastp', self.assertEqual)

    def test_blastn(self):
        run_blast('blastn', self.assertEqual)

    def test_tblastn(self):
        run_blast('tblastn', self.assertEqual)

    def test_tblastx(self):
        run_blast('tblastx', self.assertEqual)

    def test_blastx(self):
        run_blast('blastx', self.assertEqual)


def run_blast(program, assertEqual):
    args_list = generate_blast_args(program)
    run_commands(args_list, assertEqual)


def generate_blast_args(program):
    input_file_dir = path.join(settings.PROJECT_ROOT, 'example', 'blastdb/')
    output_file_dir = path.join(settings.PROJECT_ROOT, 'test_' + program + '/')
    asn_filename = path.join(output_file_dir,  'test_' + program + '.asn')
    if program == 'blastp':
        query_filename = path.join(input_file_dir, 'Cimex_sample_pep_query.faa')
        db_list = path.join(input_file_dir, 'clec_peptide_example_BLASTdb.fa')
        options = {
            'max_target_seqs': '100',
            'evalue': '10.0',
            'word_size': '6',
            'matrix': 'BLOSUM62',
            'threshold': '11',
            'gapopen': '11',
            'gapextend': '1',
            'low_complexity': 'no',
            'soft_masking': 'false',
        }
    elif program == 'blastn':
        query_filename = path.join(input_file_dir, 'LFUL_sample_query.fna')
        db_list = path.join(input_file_dir, 'Ladonda_sample_CDS_BLASTdb.fna')
        options = {
            'max_target_seqs': '100',
            'evalue': '10.0',
            'word_size': '11',
            'reward': '2',
            'penalty': '-3',
            'gapopen': '5',
            'gapextend': '2',
            'strand': 'both',
            'low_complexity': 'yes',
            'soft_masking': 'true',
        }
    elif program == 'tblastn':
        query_filename = path.join(input_file_dir, 'Cimex_sample_pep_query.faa')
        db_list = path.join(input_file_dir, 'Ladonda_sample_CDS_BLASTdb.fna')
        options = {
            'max_target_seqs': '100',
            'evalue': '10.0',
            'word_size': '6',
            'matrix': 'BLOSUM62',
            'threshold': '13',
            'gapopen': '11',
            'gapextend': '1',
            'low_complexity': 'yes',
            'soft_masking': 'false',
        }
    elif program == 'tblastx':
        query_filename = path.join(input_file_dir, 'LFUL_sample_query.fna')
        db_list = path.join(input_file_dir, 'Ladonda_sample_CDS_BLASTdb.fna')
        options = {
            'max_target_seqs': '100',
            'evalue': '10.0',
            'word_size': '3',
            'matrix': 'BLOSUM62',
            'threshold': '13',
            'strand': 'both',
            'low_complexity': 'yes',
            'soft_masking': 'false',
        }
    elif program == 'blastx':
        query_filename = path.join(input_file_dir, 'LFUL_sample_query.fna')
        db_list = path.join(input_file_dir, 'clec_peptide_example_BLASTdb.fa')
        options = {
            'max_target_seqs': '100',
            'evalue': '10.0',
            'word_size': '6',
            'matrix': 'BLOSUM62',
            'threshold': '12',
            'strand': 'both',
            'gapopen': '11',
            'gapextend': '1',
            'low_complexity': 'no',
            'soft_masking': 'false',
        }
    if path.exists(output_file_dir):
        rmtree(output_file_dir)
    makedirs(output_file_dir)
    bin_name = get_bin_name()
    program_path = path.join(settings.PROJECT_ROOT, 'blast', bin_name, program)
    blast_customized_options = {'blastn':['max_target_seqs', 'evalue', 'word_size', 'reward', 'penalty', 'gapopen', 'gapextend', 'strand', 'low_complexity', 'soft_masking'],
                                'tblastn':['max_target_seqs', 'evalue', 'word_size', 'matrix', 'threshold', 'gapopen', 'gapextend', 'low_complexity', 'soft_masking'],
                                'tblastx':['max_target_seqs', 'evalue', 'word_size', 'matrix', 'threshold', 'strand', 'low_complexity', 'soft_masking'],
                                'blastp':['max_target_seqs', 'evalue', 'word_size', 'matrix', 'threshold', 'gapopen', 'gapextend', 'low_complexity', 'soft_masking'],
                                'blastx':['max_target_seqs', 'evalue', 'word_size', 'matrix', 'threshold', 'strand', 'gapopen', 'gapextend', 'low_complexity', 'soft_masking']}
    input_opt = []
    max_target_seqs = options.get('max_target_seqs','50')
    for blast_option in blast_customized_options[program]:
        if blast_option == 'low_complexity':
            if program == 'blastn':
                input_opt.extend(['-dust', options['low_complexity']])
            else:
                input_opt.extend(['-seg', options['low_complexity']])
        else:
            input_opt.extend(['-'+blast_option, options[blast_option]])

    args_list = [[program_path, '-query', query_filename, '-db', db_list, '-outfmt', '11', '-out', asn_filename, '-num_threads', '2']]
    args_list[0].extend(input_opt)
    blast_formatter_path = path.join(settings.PROJECT_ROOT, 'blast', bin_name, 'blast_formatter')
    blast_col_name = 'qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore nident qcovs qlen slen qframe sframe'
    blast_info = {
        'col_types': ['str', 'str', 'float', 'int', 'int', 'int', 'int', 'int', 'int', 'int', 'float', 'float', 'int', 'int', 'int', 'int', 'int', 'int'],
        'col_names': blast_col_name.split(),
        'ext': {
            '.0': '0',
            '.html': '0',
            '.1': '1',
            '.3': '3',
            '.xml': '5',
            '.tsv': '6 ' + blast_col_name,
            '.csv': '10 ' + blast_col_name,
        },
    }
    for ext, outfmt in blast_info['ext'].items():
        args = [blast_formatter_path, '-archive', asn_filename, '-outfmt', outfmt, '-out', output_file_dir + 'test_' + program + ext]
        if ext == '.html':
            args.append('-html')
        if int(outfmt.split()[0]) > 4:
            args.extend(['-max_target_seqs', max_target_seqs])
        else:
            args.extend(['-num_descriptions', max_target_seqs, '-num_alignments', max_target_seqs])
        args_list.append(args)
    return args_list

def run_commands(args_list, assertEqual):
    for args in args_list:
        p = Popen(args, stdin=PIPE, stdout=PIPE)
        p.wait()
        assertEqual(p.returncode, 0)

class QueryTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(self):
        super(QueryTestCase, self).setUpClass()
        settings.DEBUG = True
        Organism.objects.create(
            display_name=display_name, short_name=short_name,
            tax_id=tax_id)
        organism = Organism.objects.get(short_name=short_name)
        sequence = SequenceType.objects.create(
            molecule_type='prot', dataset_type=dataset_type)
        prepare_test_fasta_file()
        self.files = test_files
        BlastDb.objects.create(
            fasta_file=FileObject('/blast/db/clec_peptide_example_BLASTdb.fa'),
            organism=organism, type=sequence, is_shown=False, title=title)
        organism = Organism.objects.get(short_name=short_name)
        blastdb = BlastDb.objects.get(organism=organism)
        returncode, error, output = blastdb.makeblastdb()
        returncode, error, output = blastdb.index_fasta()
        blastdb.is_shown = True
        blastdb.save()
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

    @classmethod
    def tearDownClass(self):
        self.driver.close()
        super(QueryTestCase, self).tearDownClass()

class ValidQueryTestCase(QueryTestCase):
    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test(self):
        query = ( '>Sample_Query_CLEC000107-RA\n'
        'MFYFKNLTEKVIYVKKKKNENTIVMYTQNTRVVNNARREGVPITTQQKWGGGQNKQHFPVKNTAKLDQET'
        'EELKHKTIPLSLGKLIQKERMAKGWSQKEFATKCNEKPQVVNDYEAGRGIPNQAIIGKMERVLGKIRRNV'
        'TQAEGCRNYQSKNYSKSIQQ*')
        send_query(query, self.driver, self.live_server_url)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'query-canvas-name')))

class QueryWithNoHitTestCase(QueryTestCase):
    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test(self):
        send_query('abc123', self.driver, self.live_server_url)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))
        self.assertEqual(self.driver.find_element_by_tag_name('h2').text, 'No Hits Found')

def send_query(query, driver, live_server_url):
    driver.get('%s%s' % (live_server_url, '/blast/'))
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, 'test')))
    element = driver.find_element_by_id('test')
    all_checkbox = driver.find_element_by_class_name('all-organism-checkbox')
    hover = ActionChains(driver).move_to_element(all_checkbox).move_to_element(element)
    hover.perform()
    wait.until(EC.element_to_be_clickable((By.ID, title)))
    driver.find_element_by_id(title).click()
    driver.find_element_by_id('query-textarea').send_keys(query)
    driver.find_element_by_xpath('//div//input[@value="Search"]').click()

class UploadFileTestCase(QueryTestCase):
    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test(self):
        self.driver.get('%s%s' % (self.live_server_url, '/blast/'))
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.ID, 'test')))
        element = self.driver.find_element_by_id('test')
        all_checkbox = self.driver.find_element_by_class_name('all-organism-checkbox')
        hover = ActionChains(self.driver).move_to_element(all_checkbox).move_to_element(element)
        hover.perform()
        wait.until(EC.element_to_be_clickable((By.ID, title)))
        self.driver.find_element_by_id(title).click()
        example_file_path = path.join(settings.PROJECT_ROOT, 'example', 'blastdb', 'Cimex_sample_pep_query.faa')
        self.driver.find_element_by_name('query-file').send_keys(example_file_path)
        self.driver.find_element_by_xpath('//div//input[@value="Search"]').click()
        wait.until(EC.presence_of_element_located((By.ID, 'query-canvas-name')))

class JbrowseLinkOutTestCase(QueryTestCase):
    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test(self):
        organism = Organism.objects.get(short_name=short_name)
        blast_db = BlastDb.objects.get(organism=organism)
        JbrowseSetting.objects.create(blast_db=blast_db, url='https://www.google.com/')
        query = ( '>Sample_Query_CLEC000107-RA\n'
        'MFYFKNLTEKVIYVKKKKNENTIVMYTQNTRVVNNARREGVPITTQQKWGGGQNKQHFPVKNTAKLDQET'
        'EELKHKTIPLSLGKLIQKERMAKGWSQKEFATKCNEKPQVVNDYEAGRGIPNQAIIGKMERVLGKIRRNV'
        'TQAEGCRNYQSKNYSKSIQQ*')
        send_query(query, self.driver, self.live_server_url)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'query-canvas-name')))
        # find jbrowse link out html element and get the url
        href = self.driver.find_element_by_xpath('//*[@id="results-table"]/tbody/tr[1]/td[1]/a').get_attribute("href")
        if DEBUG:
            print(href)
        self.assertEqual('/'.join(href.split('/')[:3]), 'https://www.google.com/'[:-1])
