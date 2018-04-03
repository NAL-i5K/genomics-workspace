from sys import platform


def get_bin_name():
    bin_name = 'bin_linux'
    if platform == 'darwin':
        bin_name = 'bin_mac'
    return bin_name
