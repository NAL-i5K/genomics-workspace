from django.core import management
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

class Command(BaseCommand):

    def handle(self, *args, **options):

        blast_file_name = "GCF_003254395.2_Amel_HAv3.1_genomic.fna"
        try:
            management.call_command("makemigrations")
            management.call_command("migrate")
            management.call_command("addorganism", "Apis", "mellifera")
            try:
                management.call_command("addblast", "Apis", "mellifera", "-t", "nucleotide", "Genome","Assembly", "-f", blast_file_name)
            except IntegrityError as key_error:
                msg = key_error.args[0].split("\n")[1]
                self.stdout.write("[warning]: {}, continuing to seed the blast database".format(msg))

            management.call_command("blast_utility", blast_file_name, "-m")
            management.call_command("blast_utility", blast_file_name ,"-p")
            management.call_command("blast_shown", blast_file_name, "--shown", "true")
        except Exception as e:
            raise(e)