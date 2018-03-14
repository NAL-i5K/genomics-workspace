from __future__ import print_function
from os import remove, mkdir, chmod
from os.path import dirname, abspath, join, exists
import stat as Perm
from sys import platform
from shutil import rmtree, move
import tarfile
from six.moves import urllib
from util.get_bin_name import get_bin_name

PROJECT_ROOT = dirname(abspath(__file__))

bin_name = get_bin_name()

blast_bin_path = join(PROJECT_ROOT, 'blast', bin_name + '/')

# delete old files if exist
if exists(blast_bin_path):
    rmtree(blast_bin_path)

blast_local_file_path = join(PROJECT_ROOT, 'blast.tar.gz')
if exists(blast_local_file_path):
    remove(blast_local_file_path)

extracted_blast_path = join(PROJECT_ROOT, 'ncbi-blast-2.7.1+')
if exists(extracted_blast_path):
    rmtree(extracted_blast_path)

# download the blast binary
if platform == 'darwin':
    urllib.request.urlretrieve(
        ('https://ftp.ncbi.nlm.nih.gov/blast/executables/'
         'blast+/2.7.1/ncbi-blast-2.7.1+-x64-macosx.tar.gz'),
        blast_local_file_path)
else:  # for linux
    urllib.request.urlretrieve(
        ('https://ftp.ncbi.nlm.nih.gov/blast/executables/'
         'blast+/2.7.1/ncbi-blast-2.7.1+-x64-linux.tar.gz'),
        blast_local_file_path)

# extract tar.gz file
tar = tarfile.open(blast_local_file_path, "r:gz")
tar.extractall()
tar.close()

# move bin file to specific path
move(join(extracted_blast_path, 'bin'), blast_bin_path)

# remove downloaded .gz file
if exists(blast_local_file_path):
    remove(blast_local_file_path)

if exists(extracted_blast_path):
    rmtree(extracted_blast_path)

if platform == 'darwin':
    # installation of hmmer
    hmmer_bin_path = join(PROJECT_ROOT, 'hmmer', bin_name + '/')

    if exists(hmmer_bin_path):
        rmtree(hmmer_bin_path)

    hmmer_local_file_path = join(PROJECT_ROOT, 'hmmer.tar.gz')

    if exists(hmmer_local_file_path):
        remove(hmmer_local_file_path)

    extracted_hmmer_path = join(PROJECT_ROOT, 'hmmer-3.1b2-macosx-intel')
    if exists(extracted_hmmer_path):
        rmtree(extracted_hmmer_path)

    urllib.request.urlretrieve(
        ('http://eddylab.org/software/hmmer3'
         '/3.1b2/hmmer-3.1b2-macosx-intel.tar.gz'),
        hmmer_local_file_path)

    tar = tarfile.open(hmmer_local_file_path, "r:gz")
    tar.extractall()
    tar.close()

    move(join(extracted_hmmer_path, 'binaries'), hmmer_bin_path)

    if exists(hmmer_local_file_path):
        remove(hmmer_local_file_path)

    if exists(extracted_hmmer_path):
        rmtree(extracted_hmmer_path)

    # installation of clustal
    clustal_bin_path = join(PROJECT_ROOT, 'clustal', bin_name + '/')

    if exists(clustal_bin_path):
        rmtree(clustal_bin_path)
    mkdir(clustal_bin_path)

    clustalo_path = join(clustal_bin_path, 'clustalo')

    urllib.request.urlretrieve(
        'http://www.clustal.org/omega/clustal-omega-1.2.3-macosx',
        clustalo_path)
    chmod(clustalo_path, Perm.S_IXUSR | Perm.S_IXGRP | Perm.S_IXOTH)

else:  # for linux
    # installation of hmmer
    hmmer_bin_path = join(PROJECT_ROOT, 'hmmer', bin_name + '/')

    if exists(hmmer_bin_path):
        rmtree(hmmer_bin_path)

    hmmer_local_file_path = join(PROJECT_ROOT, 'hmmer.tar.gz')

    if exists(hmmer_local_file_path):
        remove(hmmer_local_file_path)

    extracted_hmmer_path = join(PROJECT_ROOT, 'hmmer-3.1b2-linux-intel-x86_64')
    if exists(extracted_hmmer_path):
        rmtree(extracted_hmmer_path)

    urllib.request.urlretrieve(
        ('http://eddylab.org/software/hmmer3'
         '/3.1b2/hmmer-3.1b2-linux-intel-x86_64.tar.gz'),
        hmmer_local_file_path)

    tar = tarfile.open(hmmer_local_file_path, "r:gz")
    tar.extractall()
    tar.close()

    move(join(extracted_hmmer_path, 'binaries'), hmmer_bin_path)

    if exists(hmmer_local_file_path):
        remove(hmmer_local_file_path)

    if exists(extracted_hmmer_path):
        rmtree(extracted_hmmer_path)

    # installation of clustal
    clustal_bin_path = join(PROJECT_ROOT, 'clustal', bin_name + '/')

    clustalo_path = join(clustal_bin_path, 'clustalo')
    if exists(clustalo_path):
        remove(clustalo_path)

    urllib.request.urlretrieve(
        'http://www.clustal.org/omega/clustalo-1.2.4-Ubuntu-x86_64',
        clustalo_path)
    chmod(clustalo_path, Perm.S_IXUSR | Perm.S_IXGRP | Perm.S_IXOTH)
