# Generate files used in blast/tests.py
# Usage (at the root of the repo): python make_blastdb_for_tests.py
from os.path import abspath, dirname, join
from sys import platform
from subprocess import Popen, PIPE

PROJECT_ROOT = dirname(dirname(abspath(__file__)))

bin_name = 'bin_linux'
if platform == 'win32':
    bin_name = 'bin_win'
elif platform == 'darwin':
    bin_name = 'bin_mac'

makeblastdb_path = join(PROJECT_ROOT, 'blast', bin_name, 'makeblastdb')
blastdb_example_dir = join(PROJECT_ROOT, 'example', 'blastdb/')

args_list = [
    [makeblastdb_path, '-in', join(blastdb_example_dir, 'clec_peptide_example_BLASTdb.fa'), '-dbtype', 'prot', '-hash_index', '-title', 'test_Cimex', '-taxid', '79782'],
    [makeblastdb_path, '-in', join(blastdb_example_dir, 'Ladonda_sample_CDS_BLASTdb.fna'), '-dbtype', 'nucl', '-hash_index', '-title', 'test_Cimex', '-taxid', '123851'],
]

for args in args_list:
    p = Popen(args, stdout=PIPE, stderr=PIPE)
    assert p.stderr.read() == ''
