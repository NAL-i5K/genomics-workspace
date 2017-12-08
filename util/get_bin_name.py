from sys import platform


def get_bin_name():
    bin_name = 'bin_linux'
    if platform == 'darwin':
        bin_name = 'bin_mac'
    elif platform == 'win32':
        bin_name = 'bin_win'
    return bin_name
