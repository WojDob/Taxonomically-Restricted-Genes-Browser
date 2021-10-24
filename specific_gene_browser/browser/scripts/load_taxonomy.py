import csv
from pprint import pprint
from django.conf import settings
import os
from browser.models import Taxon
import time
from browser import choices
"""
To run: 
    ./manage.py runscript load_taxonomy --script-args ~/Downloads/metadata/bac120_metadata_r202.tsv

"""


def run(*args):
    # TODO: Add database wipe before every run?

    check_if_taxons_are_loaded()
    load_taxons(args[0])


def load_taxons(filepath):

    tsv_file = open(filepath)
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    next(read_tsv)  # Skip the first 'title' row.

    taxonomy_symbols = {
        "d": choices.UNIT_DOMAIN,
        "p": choices.UNIT_PHYLUM,
        "c": choices.UNIT_CLASS,
        "o": choices.UNIT_ORDER,
        "f": choices.UNIT_FAMILY,
        "g": choices.UNIT_GENUS,
        "s": choices.UNIT_SPECIES,
    }

    start = time.time()

    for counter, row in enumerate(read_tsv):
        tree = row[16].split(";")
        protein_count = row[88]
        accession = row[0]

        for i in range(len(tree)):
            if i == 0:
                previous_record, created = Taxon.objects.get_or_create(
                    name=tree[i][3:],
                    taxonomic_unit=taxonomy_symbols[tree[i][0]],
                    parent=None,
                )
            else:
                # if current taxon is a species, add protein count
                if tree[i][0] == "s":
                    previous_record, created = Taxon.objects.get_or_create(
                        name=tree[i][3:],
                        taxonomic_unit=taxonomy_symbols[tree[i][0]],
                        parent=previous_record,
                        protein_count=protein_count,
                        accession=accession
                    )
                else:
                    previous_record, created = Taxon.objects.get_or_create(
                        name=tree[i][3:],
                        taxonomic_unit=taxonomy_symbols[tree[i][0]],
                        parent=previous_record,
                    )

        if counter % 2500 == 0:
            print_stats(counter, start)
    tsv_file.close()


def check_if_taxons_are_loaded():
    if Taxon.objects.count() > 0:
        print("\033[91m\n" + "Taxons in database, aborting" + "\n\033[0m")
        exit()


def print_stats(counter, start):
    print(counter)
    print("Elapsed time:")
    end = time.time()
    print(end - start)
