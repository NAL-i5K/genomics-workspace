import os
from shutil import copyfile
from django.test import SimpleTestCase, TestCase, override_settings
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import LiveServerTestCase
# For newer django version
# from django.test import LiveServerTestCase
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from filebrowser.base import FileObject
from .models import SequenceType, BlastDb, Sequence
from app.models import Organism

display_name = 'test'
short_name = 'test'
tax_id = 217634
dataset_type = 'abc'
title = 'test'
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

peptide_seq = ( ">CLEC010822-PA:polypeptide ,Heat shock protein 70-2\\n"
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

class FrontEndTestCase(SimpleTestCase):
    @classmethod
    def setUpClass(self):
        super(FrontEndTestCase, self).setUpClass()
        # headless chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200x600')
        self.driver = webdriver.Chrome(chrome_options=options)
        # To use with header
        # self.driver = webdriver.Chrome()
        # Or use different webdriver
        # self.driver = webdriver.PhantomJS()
        # self.driver = webdriver.Firefox()
        self.driver.set_window_size(1024, 768)
        self.driver.get("http://127.0.0.1:8000/blast/test/")
        WebDriverWait(self.driver, 2)

    @classmethod
    def tearDownClass(self):
        super(FrontEndTestCase, self).tearDownClass()
        self.driver.close()

class TestClickAll(FrontEndTestCase):
    def test_click_all_organism(self):
        # self.driver.get(self.driver.current_url)
        wait = WebDriverWait(self.driver, 2) # wait at most 2 seconds to let page load, or timeout exception
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "all-organism-checkbox")))
        # click the checkbox for all-organism
        all_checkbox = self.driver.find_element_by_class_name("all-organism-checkbox")
        all_checkbox.click()
        # Find all checkboxs of all organisms and check if they are all selected
        organism_checkboxs = self.driver.find_elements_by_class_name("organism-checkbox")
        for c in organism_checkboxs:
            self.assertEqual(c.is_selected(), True)
        self.assertEqual(self.driver.find_element_by_css_selector("input.all-dataset-checkbox.nucleotide.genome-assembly").is_selected(), True)
        self.assertEqual(bool(self.driver.find_element_by_css_selector("input.all-dataset-checkbox.peptide.protein").get_attribute("disabled")), True)
        # unselect the checkbox for all-organism
        all_checkbox.click()
        for c in organism_checkboxs:
            self.assertEqual(c.is_selected(), False)
        self.assertEqual(self.driver.find_element_by_css_selector("input.all-dataset-checkbox.nucleotide.genome-assembly").is_selected(), False)
        self.assertEqual(bool(self.driver.find_element_by_css_selector("input.all-dataset-checkbox.peptide.protein").get_attribute("disabled")), False)

class TestNucleotideSequenceSimple(FrontEndTestCase):
    def test_input_sequence(self):
        wait = WebDriverWait(self.driver, 2) # wait at most 2 seconds to let page load, or timeout exception
        wait.until(EC.element_to_be_clickable((By.ID, "query-textarea")))
        # Insert sample nucleotide into textarea
        # Don't use send_keys(peptide_seq), since it's too slow
        self.driver.execute_script("$('#query-textarea').val(\"" + nucleotide_seq + "\").keyup();")
        checkProgramOptions(self.driver, self.assertEqual, selected=[True, False, False, False, False], disabled=[False, True, False, True, False])
        reset_button = self.driver.find_element_by_css_selector("input.btn_reset")
        reset_button.click()
        checkProgramOptions(self.driver, self.assertEqual, selected=[True, False, False, False, False], disabled=[False, False, False, False, False])

class TestNucleotideSequenceComplex(FrontEndTestCase):
    def test_input_sequence(self):
        wait = WebDriverWait(self.driver, 2) # wait at most 2 seconds to let page load, or timeout exception
        wait.until(EC.element_to_be_clickable((By.ID, "query-textarea")))
        # Insert sample nucleotide into textarea
        # Don't use send_keys(peptide_seq), since it's too slow
        self.driver.execute_script("$('#query-textarea').val(\"" + nucleotide_seq + "\").keyup(); $('#query-textarea').val('').keyup();")
        checkProgramOptions(self.driver, self.assertEqual, selected=[True, False, False, False, False], disabled=[False, False, False, False, False])

class TestPeptideSequenceSimple(FrontEndTestCase):
    def test_input_sequence(self):
        wait = WebDriverWait(self.driver, 2) # wait at most 2 seconds to let page load, or timeout exception
        wait.until(EC.element_to_be_clickable((By.ID, "query-textarea")))
        # Insert sample peptide into textarea
        # Don't use send_keys(peptide_seq), since it's too slow
        self.driver.execute_script("$('#query-textarea').val('" + peptide_seq + "').keyup();")
        checkProgramOptions(self.driver, self.assertEqual, selected=[False, True, False, False, False], disabled=[True, False, True, False, True])
        reset_button = self.driver.find_element_by_css_selector("input.btn_reset")
        reset_button.click()
        checkProgramOptions(self.driver, self.assertEqual, selected=[True, False, False, False, False], disabled=[False, False, False, False, False])

class TestPeptideSequenceComplex(FrontEndTestCase):
    def test_input_sequence(self):
        wait = WebDriverWait(self.driver, 2) # wait at most 2 seconds to let page load, or timeout exception
        wait.until(EC.element_to_be_clickable((By.ID, "query-textarea")))
        # Insert sample peptide into textarea
        # Don't use send_keys(peptide_seq), since it's too slow
        self.driver.execute_script("$('#query-textarea').val('" + peptide_seq + "').keyup(); $('#query-textarea').val('').keyup();")
        checkProgramOptions(self.driver, self.assertEqual, selected=[True, False, False, False, False], disabled=[False, False, False, False, False])

class TestLoadExampleNucleotideSequence(FrontEndTestCase):
    def test_load_example_sequence(self):
        wait = WebDriverWait(self.driver, 2) # wait at most 2 seconds to let page load, or timeout exception
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.load-nucleotide.txt")))
        self.driver.find_element_by_css_selector("span.load-nucleotide.txt").click()
        checkProgramOptions(self.driver, self.assertEqual, selected=[True, False, False, False, False], disabled=[False, True, False, True, False])

class TestLoadExamplePeptideSequence(FrontEndTestCase):
    def test_load_example_sequence(self):
        wait = WebDriverWait(self.driver, 2) # wait at most 2 seconds to let page load, or timeout exception
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.load-peptide.txt")))
        self.driver.find_element_by_css_selector("span.load-peptide.txt").click()
        checkProgramOptions(self.driver, self.assertEqual, selected=[False, True, False, False, False], disabled=[True, False, True, False, True])

class TestClickSequenceType(FrontEndTestCase):
    def test_click_sequence_type(self):
        wait = WebDriverWait(self.driver, 2) # wait at most 2 seconds to let page load, or timeout exception
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
        # protein.click()

class TestHoverIntent(FrontEndTestCase):
    def test_hover_intent(self):
        wait = WebDriverWait(self.driver, 2) # wait at most 2 seconds to let page load, or timeout exception
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

def checkSeqenceTypes(driver, assertEqual, selected=[False, False, False], disabled=[False, False, False]):
    assembly = driver.find_element_by_css_selector("input.all-dataset-checkbox.nucleotide.genome-assembly")
    transcript = driver.find_element_by_css_selector("input.all-dataset-checkbox.nucleotide.transcript")
    protein = driver.find_element_by_css_selector("input.all-dataset-checkbox.protein.peptide")
    # check if selected
    assertEqual(assembly.is_selected(), selected[0])
    assertEqual(transcript.is_selected(), selected[1])
    assertEqual(protein.is_selected(), selected[2])
    # check if disabled
    assertEqual(bool(assembly.get_attribute("disabled")), disabled[0])
    assertEqual(bool(transcript.get_attribute("disabled")), disabled[1])
    assertEqual(bool(protein.get_attribute("disabled")), disabled[2])

class BlastModelTest(TestCase):
    def setUp(self):
        Organism.objects.create(display_name=display_name, short_name=short_name, tax_id=tax_id)
        organism = Organism.objects.get(short_name=display_name)
        sequence = SequenceType.objects.create(molecule_type='prot', dataset_type=dataset_type)
        prepare_test_fasta_file()
        self.files = test_files
        BlastDb.objects.create(fasta_file=FileObject('/blast/db/clec_peptide_example_BLASTdb.fa'), organism=organism, type=sequence, is_shown=False, title=title)

    def test_makeblastdb(self):
        organism = Organism.objects.get(short_name=short_name)
        blastdb = BlastDb.objects.get(organism=organism)
        returncode, error, output = blastdb.makeblastdb()
        self.assertEqual(returncode, 0)
        self.assertEqual(error, '')
        for file in self.files:
            self.assertEqual(os.path.exists(os.path.join(settings.PROJECT_ROOT, 'media/blast/db/', file)), True)

    def test_index_fasta(self):
        organism = Organism.objects.get(short_name=short_name)
        blastdb = BlastDb.objects.get(organism=organism)
        returncode, error, output = blastdb.index_fasta()
        self.assertEqual(returncode, 0)
        self.assertEqual(error, '')
        self.assertEqual(blastdb.title, 'test')
        all_sequence = Sequence.objects.all()
        self.assertEqual(len(all_sequence), 395)
        for s in all_sequence:
            self.assertEqual(s.blast_db.title, 'test')

class BlastAdminTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(self):
        super(BlastAdminTestCase, self).setUpClass()
        settings.DEBUG = True
        User = get_user_model()
        self.username = 'test'
        self.password = 'test'
        User.objects.create_superuser(username=self.username, password=self.password, email='test@test.com')
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
        super(BlastAdminTestCase, self).tearDownClass()
        self.driver.close()

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_setup_is_shown(self):
        self.driver.get('%s%s' % (self.live_server_url, '/admin/'))
        wait = WebDriverWait(self.driver, 5) # wait at most 5 seconds to let page load, or timeout exception
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
        description_input = self.driver.find_element_by_id('id_description')
        tax_id_input = self.driver.find_element_by_id('id_tax_id')
        display_name_input.send_keys(display_name)
        # check auto fill-in short name should be the same as display name
        self.assertEqual(short_name_input.get_attribute('value'), display_name)
        # TODO: check functionality of automatically fetching tax_id and description
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
        self.driver.get('%s%s' % (self.live_server_url, '/blast/'))
        wait.until(EC.element_to_be_clickable((By.ID, 'test')))
        element = self.driver.find_element_by_id('test')
        all_checkbox = self.driver.find_element_by_class_name('all-organism-checkbox')
        hover = ActionChains(self.driver).move_to_element(all_checkbox).move_to_element(element)
        hover.perform()
        wait.until(EC.element_to_be_clickable((By.ID, 'clec_peptide_example_BLASTdb.fatest')))
        self.driver.find_element_by_id('clec_peptide_example_BLASTdb.fatest').click()
        example_query = ( '>Sample_Query_CLEC000107-RA\n'
        'MFYFKNLTEKVIYVKKKKNENTIVMYTQNTRVVNNARREGVPITTQQKWGGGQNKQHFPVKNTAKLDQET'
        'EELKHKTIPLSLGKLIQKERMAKGWSQKEFATKCNEKPQVVNDYEAGRGIPNQAIIGKMERVLGKIRRNV'
        'TQAEGCRNYQSKNYSKSIQQ*')
        self.driver.find_element_by_id('query-textarea').send_keys(example_query)
        self.driver.find_element_by_xpath('//div//input[@value="Search"]').click()
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'query-canvas-name')))

def prepare_test_fasta_file():
    for file in test_files:
        if os.path.exists(os.path.join(settings.PROJECT_ROOT, 'media/blast/db/', file)):
            os.remove(os.path.join(settings.PROJECT_ROOT, 'media/blast/db/', file))
    copyfile(os.path.join(settings.PROJECT_ROOT, 'example/blastdb/clec_peptide_example_BLASTdb.fa'), os.path.join(settings.PROJECT_ROOT, 'media/blast/db/clec_peptide_example_BLASTdb.fa'))
