from __future__ import print_function
from os import remove
from os.path import dirname, abspath, join, exists
from sys import platform
from shutil import rmtree, move
import tarfile
from six.moves import urllib

PROJECT_ROOT = dirname(abspath(__file__))

bin_name = 'bin_linux'
if platform == 'win32':
    bin_name = 'bin_win'
elif platform == 'darwin':
    bin_name = 'bin_mac'

bin_path = join(PROJECT_ROOT, 'blast/', bin_name + '/')
# delete old files if exist
if exists(bin_path):
    rmtree(bin_path)

local_file_path = join(PROJECT_ROOT, 'blast.tar.gz')
if exists(local_file_path):
    remove(local_file_path)

extracted_blast_path = join(PROJECT_ROOT, 'ncbi-blast-2.6.0+')
if exists(extracted_blast_path):
    rmtree(extracted_blast_path)
# download the blast binary
if platform == 'win32':
    urllib.request.urlretrieve(
        ('https://ftp.ncbi.nlm.nih.gov/blast/executables/'
            'blast+/2.6.0/ncbi-blast-2.6.0+-x64-win64.tar.gz'),
        local_file_path)
elif platform == 'darwin':
    urllib.request.urlretrieve(
        ('https://ftp.ncbi.nlm.nih.gov/blast/executables/'
            'blast+/2.6.0/ncbi-blast-2.6.0+-x64-macosx.tar.gz'),
        local_file_path)
else:  # for linux
    urllib.request.urlretrieve(
        ('https://ftp.ncbi.nlm.nih.gov/blast/executables/'
            'blast+/2.6.0/ncbi-blast-2.6.0+-x64-linux.tar.gz'),
        local_file_path)
# extract tar.gz file
tar = tarfile.open(local_file_path, "r:gz")
tar.extractall()
tar.close()
# move bin file to specific path
move(join(extracted_blast_path, 'bin'), bin_path)
