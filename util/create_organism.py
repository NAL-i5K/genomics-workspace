from app.models import Organism

# TODO: feed following information through command line arugments or read from a file

tax_id = 438503

display_name = 'Catajapyx aquilonaris'
short_name = 'cataaquil'
description = 'The japygid Catajapyx aquilonaris is a blind predator of the soil. Like Protura (Acerentomon maius) and Collembola (Sminthurus viridis), Diplura lack wings, mirroring the wingless insect ancestor. Like in all primarily wingless hexapods, sperms are not transferred directly during copulation. Males rather deposit a spermatophore on the ground and females subsequently take the spermatophore up. Diplura are critical for understanding the evolutionary origin of Hexapoda (e.g., terrestrialization), the evolutionary origin of wings (ancestral condition in Diplura), and the evolution of direct sperm transfer (ancestral condition in Diplura).'


# TODO: autogenerate short name / autogenerate tax_id / pull the description from wiki like we did in the GUI

new_org = Organism(display_name=display_name, short_name=short_name, description=description, tax_id=tax_id)
new_org.save()
