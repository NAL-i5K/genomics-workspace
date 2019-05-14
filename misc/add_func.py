from blast.models import BlastDb, SequenceType
#from django.core.management.base import BaseCommand, CommandError
from app.models import Organism
#import requests
import os
import sys
import requests

def display_name(options):

    base = options['Genus_Species'][0].lower().capitalize() + ' ' + options['Genus_Species'][1].lower()
    if len(options['Genus_Species']) == 3:
        display_name = base + ' '+ options['Genus_Species'][2].lower()
        return display_name

    else:
        display_name = base
        return display_name

def get_organism(display_name):

    organism_database = Organism.objects.get(display_name = display_name)
    if organism_database :
        return organism_database
    else:
        print("check your organism name again if it still fails then check your organism database")
        sys.exit(0)

def get_path(app_name,title):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if app_name == 'blast':
        path = os.path.join('blast/db',title)
    else:
        path = os.path.join('hmmer/db',title)

    a=os.path.join(base_dir,'media',path)
    check = os.path.isfile(a)
    if check:
        return path
    else:
        print("No fasta file in media/blast/db or media/hmmer/db")
        sys.exit(0)

def short_name(name):
    short_name = name.split(' ')
    short_name1 = short_name[0][0:3]
    short_name2 = short_name[1][0:3]
    short_name = short_name1 + short_name2
    return short_name

def get_molecule(options):
    try:
        molecule = options['type'][0].lower() #get molecule_type from command line
        if molecule == 'peptide':    #change the name tp prot or nucl
            molecule2 = 'prot'
        elif molecule == 'nucleotide':
            molecule2 = 'nucl'
        else:
            print("please enter the correct molecule_type, must be nucleotide or peptide")
            sys.exit(0)
    except Exception :
        print("enter the argument complete '-t' '-f' ")
        sys.exit(0)
    molecule_type = SequenceType.objects.filter(molecule_type = molecule2) #get the data from molecule_type field
    a = molecule_type[0]
    molecule_str = a.molecule_type
    return molecule2,molecule_str

def get_dataset(options):

    dataset = options['type'][1].lower().capitalize()
    if dataset =='Genome':
        dataset = dataset + ' ' + options['type'][2].lower().capitalize()
        pass
    elif dataset == 'Transcript':
        pass
    elif dataset == 'Protein':
        pass
    else:
        print('enter the correct dataset type')
        sys.exit(0)
    dataset_type = SequenceType.objects.filter(dataset_type = dataset)
    b = dataset_type[0]
    dataset_str = str(b.dataset_type)
    return dataset,dataset_str

def get_type(dataset,molecule2,molecule_str,dataset_str): #get the sequence type from SequencType Table

    if molecule2 != molecule_str :
        print("something wrong in molecule")
    elif dataset != dataset_str :
        print("something wrong with dataset")
    else:
        try:	
            dataset_type = SequenceType.objects.filter(molecule_type = molecule2, dataset_type = dataset)
            return dataset_type[0]
        except:
            print("there are no {molecule} - {dataset} combination in the database".format(molecule=molecule2.capitalize(),dataset=dataset_str))
            sys.exit(0)
        '''
        if len(dataset_type)== 0:
            print("there are no {molecule} - {dataset} combination in the database".format(molecule=molecule2.capitalize(),dataset=dataset_str))
            sys.exit(0)
        else:
            return dataset_type[0]
        '''
def get_description(url1,wiki_url2):
    try:
        re1 = requests.get(url1)
        data1 = re1.json()
        try:
            title = data1['query']['search'][0]['title']
            url2 = wiki_url2 + title
            re2 = requests.get(url2)
            data2 = re2.json()
            key = data1['query']['search'][0]['pageid']
            key = str(key)
            #print type(key)
            description = data2['query']['pages'][key]['extract']
            #print description
            return description
        except 	IndexError:
            print("check your organism name again")
            sys.exit(0)
    except requests.exceptions.ConnectionError:
        print("check your internet connection")
        sys.exit(0)

def get_taxid(id_baseurl,name):
    try:
        url = id_baseurl+ name
        re = requests.get(url)
        data = re.json()
        tax_id = data['esearchresult']['idlist'][0]
        tax_id = int(tax_id)
        return tax_id
    except IndexError:
        print("make sure your name is completed and correct")
        sys.exit(0)

def delete_func(options):
    if options["organism"]:
        organism = options["organism"][0].lower().capitalize() + " " + options["organism"][1].lower()
        organism1 = Organism.objects.filter(display_name = organism).delete()
        print organism1
        return ("remove %s in database"%organism)
    elif options["blast"]:
        blast = options["blast"][0]
        for blast in options["blast"]:
            blast = BlastDb.objects.filter(title = blast).delete()
            return blast, "remove blastdb you selected"
    elif options["hmmer"]:
        hmmer = options["hmmer"][0]
        for hmmer in options["hmmer"]:
            hmmer = HmmerDB.objects.filter(title = hmmer).delete()
            return hmmer, "remove hmmerdb you selected"
    else:
        return "please give the argument, -o to delete organism, -b to delete blastdb, -hr to delete hmmerdb"
