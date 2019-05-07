from blast.models import BlastDb
from django.core.management.base import BaseCommand
from subprocess import Popen, PIPE
from util.get_bin_name import get_bin_name
from filebrowser.fields import FileBrowseField
from django.conf import settings

class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('BlastDb',nargs='+',type=str,help='enter the blast db name')

    def handle(*args,**options):
        title = options['BlastDb'][0]
        blast = BlastDb.objects.get(title = title)
        blast.makeblastdb()
        print("done")


        ''' 
        if not os.path.isfile(blast.fasta_file.path_full):
            return 1, 'FASTA file not found', ''
        bin_name = get_bin_name()
        #print(bin_name)
        makeblastdb_path = os.path.join(settings.BASE_DIR, 'blast', bin_name, 'makeblastdb')
        #print(makeblastdb_path)
        args = [makeblastdb_path, '-in', blast.fasta_file.path_full, '-dbtype' , blast.type.molecule_type, '-hash_index'] # , '-parse_seqids' TODO: make option
        if blast.title:
            args += ['-title', blast.title]
        if blast.organism.tax_id:
            args += ['-taxid', str(blast.organism.tax_id)]
        #print(args)
        p = Popen(args, stdout=PIPE, stderr=PIPE)
        output, error = p.communicate()
        print("finish to execute the makeblastdb ")
        #return p.returncode, error, output
        '''
