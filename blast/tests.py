from django.test import SimpleTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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