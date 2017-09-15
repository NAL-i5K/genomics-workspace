from django.test import SimpleTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

seq = ( ">CLEC010822-PA:polypeptide ,Heat shock protein 70-2\\n"
        "MILHFLVLLFASALAADEKNKDVGTVVGIDLGTTYSCVGVYKNGRVEIIANDQGNRITPSYVAFTSEGERLIGDAAKNQLTTNPENTVFDAKRLIGREWTDSTVQDDIKFFPFKVLEKNSKPHIQVSTSQGNKMFAPEEISAMVLGKMKETAEAYLGKKVTHAVVTVPAYFNDAQRQATKDAGTISGLNVMRIINEPTAAAIAYGLDKKEGEKNVLVFDLGGGTFDVSLLTIDNGVFEVVSTNGDTHLGGEDFDQRVMDHFIKLYKKKKGKDIRKDNRAVQKLRREVEKAKRALSSSHQVRIEIESFYDGEDFSETLTRAKFEELNMDLFRSTMKPVQKVLEDADMNKKDVDEIVLVGGSTRIPKVQALVKEFFNGKEPSRGINPDEAVAYGAAVQAGVLSGEQDTDSIVLLDVNPLTLGIETVGGVMTKLIPRNTVIPTKKSQIFSTASDNQHTVTIQVYEGERPMTKDNHLLGKFDLTGIPPAPRGVPQIEVTFEIDANGILQVSAEDKGTGNREKIVITNDQNRLTPDDIDRMIKDAEKFADDDKKLKERVEARNELESYAYSLKNQLADKDKFGSKVTDSDKAKMEKAIEEKIKWLDENQDADSEAFKKQKKELEDVVQPIISKLYQGGAPPPPGAGPQSEDDLKDEL*\\n"
        ">OFAS004830-PA:polypeptide ,Heat shock protein 70-2\\n"
        "MAAGGSRPTRPAVGIDLGTTYSCVGYFDKGRVEIIANDQGNRVTPSYVAFTETDRIVGDAARGQAIMNPSNTVYDAKRLIGRKFDDPSVQADRKMWPFKVASKEGKPMIEVTYKGETRQFFPEEISSMVLSKMRETAESYIGKKVSNAVVTVPAYFNDSQRQATKDSGTIAGLNVLRIINEPTAAAVAYGLDKKGSGEINVLIFDLGGGTFDVSVLTIADGLFEVKATAGDTHLGGADFDNRMVQYFLEEFKRKTKKEVNDNKRALRRLQAACERAKRVLSTATQATVEIDSFVDGIDLYSAVSRAKFEEINSDLFRGTLGPVEKAIRDSKIPKNRIDEIVLVGGSTRIPKIQSLLVEYFNGKELNKTINPDEAVAYGAAVQAAIIVGDTSDEVKDVLLLDVTPLSLGIETAGGIMTNLIPRNTTIPVKHSQIFSTYSDNQPGVLIQVYEGERAMTKDNNLLGTFELRGFPPAPRGVPQIEVAFDVDANGILNVTAQEMSTKKTSKITITNDKGRLTKAQIEKMVKEAERYKSEDTAARETAEAKNGLESYCYAMKNSVEEAANLGRVTEDEMKSVVRKCNETIMWIEANRSATKMEFEKKMRETESVCKPIATKILSRGTQQNNAGGGTPTNERGPVIEEAD\\n"
        ">OFAS004738-PA:polypeptide ,Heat shock protein 70-1\\n"
        "MPAIGIDLGTTYSCVGVWQHGKVEIIANDQGNRTTPSYVAFSDTERLIGDAAKNQVAMNPQNTVFDAKRLIGRKYDDPKIQDDLKHWPFRVVDCSSKPKIQVEYKGETKTFAPEEISSMVLVKMKETAEAYLGGTVRDAVITVPAYFNDSQRQATKDAGAIAGLNVLRIINEPTAAALAYGLDKNLKGERNVLIFDLGGGTFDGPREQDHSLKGERNVLIFDLGGGTFDVSILTIDEGSLFEVKSTAGDTHLGGEDFDNRLVNHLAEEFKRKYRKDLKTNPRALRRLRTAAERAKRTLSSSTEASIEIDALFEGVDFYTKITRARFEELCSDLFRSTLQPVEKALQDAKLDKGLIHDVVLVGGSTRIPKIQNLLQNFFNGKSLNMSINPDEAVAYGAAVQAAILSGDQSSKIQDVLLVDVAPLSLGIETAGGVMTKIIERNTRI"
)

class FrontEndTestCase(SimpleTestCase):
    @classmethod
    def setUpClass(self):
        super(FrontEndTestCase, self).setUpClass()
        self.driver = webdriver.Chrome()
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

class TestInputSequenceSimple(FrontEndTestCase):
    def test_input_sequence(self):
        wait = WebDriverWait(self.driver, 2) # wait at most 2 seconds to let page load, or timeout exception
        wait.until(EC.element_to_be_clickable((By.ID, "query-textarea")))
        # Insert sample peptide into textarea
        # Don't use send_keys(seq), since it's too slow
        self.driver.execute_script("$('#query-textarea').val('" + seq + "').keyup();")
        blastn_radio = self.driver.find_element_by_css_selector("input.program.blastn")
        tblastn_radio = self.driver.find_element_by_css_selector("input.program.tblastn")
        tblastx_radio = self.driver.find_element_by_css_selector("input.program.tblastx")
        blastp_radio = self.driver.find_element_by_css_selector("input.program.blastp")
        blastx_radio = self.driver.find_element_by_css_selector("input.program.blastx")
        self.assertEqual(bool(blastn_radio.get_attribute("disabled")), True)
        self.assertEqual(blastn_radio.is_selected(), False)
        self.assertEqual(bool(tblastn_radio.get_attribute("disabled")), False)
        self.assertEqual(tblastn_radio.is_selected(), True)
        self.assertEqual(bool(tblastx_radio.get_attribute("disabled")), True)
        self.assertEqual(tblastx_radio.is_selected(), False)
        self.assertEqual(bool(blastp_radio.get_attribute("disabled")), False)
        self.assertEqual(blastp_radio.is_selected(), False)
        self.assertEqual(bool(blastx_radio.get_attribute("disabled")), True)
        self.assertEqual(blastx_radio.is_selected(), False)

class TestInputSequenceComplex(FrontEndTestCase):
    def test_input_sequence(self):
        wait = WebDriverWait(self.driver, 2) # wait at most 2 seconds to let page load, or timeout exception
        wait.until(EC.element_to_be_clickable((By.ID, "query-textarea")))
        # Insert sample peptide into textarea
        # Don't use send_keys(seq), since it's too slow
        self.driver.execute_script("$('#query-textarea').val('" + seq + "').keyup(); $('#query-textarea').val('').keyup();")
        blastn_radio = self.driver.find_element_by_css_selector("input.program.blastn")
        tblastn_radio = self.driver.find_element_by_css_selector("input.program.tblastn")
        tblastx_radio = self.driver.find_element_by_css_selector("input.program.tblastx")
        blastp_radio = self.driver.find_element_by_css_selector("input.program.blastp")
        blastx_radio = self.driver.find_element_by_css_selector("input.program.blastx")
        self.assertEqual(bool(blastn_radio.get_attribute("disabled")), False)
        self.assertEqual(blastn_radio.is_selected(), True)
        self.assertEqual(bool(tblastn_radio.get_attribute("disabled")), False)
        self.assertEqual(tblastn_radio.is_selected(), False)
        self.assertEqual(bool(tblastx_radio.get_attribute("disabled")), False)
        self.assertEqual(tblastx_radio.is_selected(), False)
        self.assertEqual(bool(blastp_radio.get_attribute("disabled")), False)
        self.assertEqual(blastp_radio.is_selected(), False)
        self.assertEqual(bool(blastx_radio.get_attribute("disabled")), False)
        self.assertEqual(blastx_radio.is_selected(), False)
        # .send_keys(seq)

class TestLoadExampleSequence(FrontEndTestCase):
    def test_load_example_sequence(self):
        wait = WebDriverWait(self.driver, 2) # wait at most 2 seconds to let page load, or timeout exception
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.load-nucleotide.txt")))
        self.driver.find_element_by_css_selector("span.load-nucleotide.txt").click()
        blastn_radio = self.driver.find_element_by_css_selector("input.program.blastn")
        tblastn_radio = self.driver.find_element_by_css_selector("input.program.tblastn")
        tblastx_radio = self.driver.find_element_by_css_selector("input.program.tblastx")
        blastp_radio = self.driver.find_element_by_css_selector("input.program.blastp")
        blastx_radio = self.driver.find_element_by_css_selector("input.program.blastx")
        self.assertEqual(bool(blastn_radio.get_attribute("disabled")), True)
        self.assertEqual(blastn_radio.is_selected(), False)
        self.assertEqual(bool(tblastn_radio.get_attribute("disabled")), False)
        self.assertEqual(tblastn_radio.is_selected(), True)
        self.assertEqual(bool(tblastx_radio.get_attribute("disabled")), True)
        self.assertEqual(tblastx_radio.is_selected(), False)
        self.assertEqual(bool(blastp_radio.get_attribute("disabled")), False)
        self.assertEqual(blastp_radio.is_selected(), False)
        self.assertEqual(bool(blastx_radio.get_attribute("disabled")), True)
        self.assertEqual(blastx_radio.is_selected(), False)