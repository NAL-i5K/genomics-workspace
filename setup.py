"""
This script will install binaries (blast, hmmer, and clustal) for genomics-workspace.
"""
from __future__ import print_function
from os import remove, mkdir, chmod
from os.path import dirname, abspath, join, exists, basename
import stat as Perm
from sys import platform
from shutil import rmtree, move, copyfile
import tarfile
import subprocess
from six.moves import urllib
from util.get_bin_name import get_bin_name
import requests

BASE_DIR = dirname(abspath(__file__))


def install_blast(bin_name):
    blast_bin_path = join(BASE_DIR, 'blast', bin_name + '/')
    # delete old files if exist
    if exists(blast_bin_path):
        print(
            'Old blast installation detected. {} will be removed and new blast copy will be installed.'.
            format(blast_bin_path))
        rmtree(blast_bin_path)

    blast_local_file_path = join(BASE_DIR, 'blast.tar.gz')
    if exists(blast_local_file_path):
        remove(blast_local_file_path)

    extracted_blast_path = join(BASE_DIR, 'ncbi-blast-2.7.1+')
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
    print('Cleaning up temp files during blast installation ...')
    if exists(blast_local_file_path):
        remove(blast_local_file_path)

    if exists(extracted_blast_path):
        rmtree(extracted_blast_path)


def install_hmmer(bin_name):
    hmmer_bin_path = join(BASE_DIR, 'hmmer', bin_name)
    if exists(hmmer_bin_path):
        print(
            'Old HMMER installation detected. {} will be removed and new HMMER copy will be installed.'.
            format(hmmer_bin_path))
        rmtree(hmmer_bin_path)
    mkdir(hmmer_bin_path)
    hmmer_local_file_path = join(hmmer_bin_path, 'hmmer-3.2-0.tar.bz2')
    if platform == 'darwin':
        download_url = ('https://anaconda.org/bioconda/hmmer/'
                        '3.2/download/osx-64/hmmer-3.2-0.tar.bz2')
    else:  # for linux
        download_url = ('https://anaconda.org/bioconda/hmmer/'
                        '3.2/download/linux-64/hmmer-3.2-0.tar.bz2')

    req = requests.get(download_url)
    with open(hmmer_local_file_path, 'wb') as f:
        for chunk in req.iter_content(100000):
            f.write(chunk)

    tar = tarfile.open(hmmer_local_file_path, 'r:bz2')
    tar.extractall(hmmer_bin_path)
    tar.close()

    # delete downloaded and generated files after installation
    print('Cleaning up temp files during hmmer installation ...')
    if exists(hmmer_local_file_path):
        remove(hmmer_local_file_path)


def install_clustal(bin_name):
    clustal_bin_path = join(BASE_DIR, 'clustal', bin_name + '/')
    if exists(clustal_bin_path):
        print(
            'Old clustal installation detected. {} will be removed and new blast copy will be installed.'.
            format(clustal_bin_path))
        rmtree(clustal_bin_path)
    mkdir(clustal_bin_path)
    clustalo_path = join(clustal_bin_path, 'clustalo')
    if exists(clustalo_path):
        remove(clustalo_path)
    clustalw_path = join(clustal_bin_path, 'clustalw2')
    if exists(clustalw_path):
        remove(clustalw_path)
    if platform == 'darwin':
        print('Installing clustalo ...')
        urllib.request.urlretrieve(
            'http://www.clustal.org/omega/clustal-omega-1.2.3-macosx',
            clustalo_path)

        print('Installing clustalw ...')
        clustalw_dmg_path = join(clustal_bin_path, 'clustalw-2.1-macosx.dmg')
        clustalw_dmg_attach_path = join('/Volumes', 'clustalw-2.1-macosx',
                                        'clustalw-2.1-macosx', 'clustalw2')
        urllib.request.urlretrieve(
            'http://www.clustal.org/download/current/clustalw-2.1-macosx.dmg',
            clustalw_dmg_path)

        subprocess.call(['hdiutil', 'attach', clustalw_dmg_path])
        copyfile(clustalw_dmg_attach_path, clustalw_path)
        subprocess.call(
            ['hdiutil', 'detach',
             join('/Volumes', 'clustalw-2.1-macosx')])
        remove(clustalw_dmg_path)
    else:  # for linux
        print('Installing clustalo ...')
        urllib.request.urlretrieve(
            'http://www.clustal.org/omega/clustalo-1.2.4-Ubuntu-x86_64',
            clustalo_path)

        clustalw_tar_path = join(
            clustal_bin_path, 'clustalw-2.1-linux-x86_64-libcppstatic.tar.gz')
        clustalw_path = join(clustal_bin_path, 'clustalw2')
        urllib.request.urlretrieve(
            'http://www.clustal.org/download/current/clustalw-2.1-linux-x86_64-libcppstatic.tar.gz',
            clustalw_tar_path)

        print('Installing clustalw ...')
        tar = tarfile.open(clustalw_tar_path, 'r:gz')
        for member in tar.getmembers():
            if member.isreg():
                member.name = basename(member.name)
                tar.extract(member, clustal_bin_path)
        tar.close()
        remove(clustalw_tar_path)

    chmod(clustalo_path, Perm.S_IXUSR | Perm.S_IXGRP | Perm.S_IXOTH)
    chmod(clustalw_path, Perm.S_IXUSR | Perm.S_IXGRP | Perm.S_IXOTH)


if __name__ == '__main__':
    bin_name = get_bin_name()
    print('Installing blast ...')
    install_blast(bin_name)
    print('Installing hmmer ...')
    install_hmmer(bin_name)
    print('Installing clustal ...')
    install_clustal(bin_name)
