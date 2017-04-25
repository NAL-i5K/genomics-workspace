'''
    get_tag

    return a search tag
'''
from blast.models import BlastSearch
from random import randint
import enchant
import json
import sys
import os

TAG_MAXTRIES = 100

VOWS = 'AEIOU'                   #  Vowel list.
CONS = 'BCDFGHJKLMNPQRSTVWXYZ'   #  Consonant list.
di   = enchant.Dict("en_US")     #  English dictionary instance.

def get_tag(prefix, classobj):
    #
    #  Get a unique random search tag in the format
    #
    #    <prefix>-<consonant><vowel><consonant><vowel>
    #
    #  not in the English dictionary, and prepend the user name to it.
    #
    while True:
        b = randint(0, 4)
        d = randint(0, 4)
        if b != d:
            #  Skip tags with the same vowels.
            break
    found = False
    for tri in range(1, TAG_MAXTRIES):
        a = randint(0, 20)
        c = randint(0, 20)
        tag = CONS[a] + VOWS[b] + CONS[c] + VOWS[d]
        if (di.check(tag)):
            #  Skip dictionary words.
            continue
        tag = prefix + '-' + tag
        if not classobj.objects.filter(search_tag=tag).exists():
            #  Make it unique.
            found = True
            break

    if tri > 50:
        log.debug("get_tag: TAG tries: ---> %d" % tri)

    if found:
        return tag
    else:
        log.error('Run out of search tags')
        return None

