import csv
from pprint import pprint
from django.conf import settings
import os
from browser.models import TaxonomicUnit, Taxon
import time

"""
To run: 
    ./manage.py runscript load_taxonomy --script-args ~/Downloads/metadata/bac120_metadata_r202.tsv

"""


def run(*args):
    # TODO: Add database wipe before every run?

    check_if_taxons_are_loaded()
    create_taxonomic_units()
    load_taxons(args[0])


def load_taxons(filepath):

    tsv_file = open(filepath)
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    next(read_tsv)  # Skip the first 'title' row.

    taxonomy_symbols = {
        "d": TaxonomicUnit.objects.get(name="Domain"),
        "p": TaxonomicUnit.objects.get(name="Phylum"),
        "c": TaxonomicUnit.objects.get(name="Class"),
        "o": TaxonomicUnit.objects.get(name="Order"),
        "f": TaxonomicUnit.objects.get(name="Family"),
        "g": TaxonomicUnit.objects.get(name="Genus"),
        "s": TaxonomicUnit.objects.get(name="Species"),
    }

    start = time.time()

    for counter, row in enumerate(read_tsv):
        tree = row[16].split(";")
        for i in range(len(tree)):
            if i == 0:
                previous_record, created = Taxon.objects.get_or_create(
                    name=tree[i][3:],
                    taxonomic_unit=taxonomy_symbols[tree[i][0]],
                    parent=None,
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


def create_taxonomic_units():
    taxonomic_units = [
        "Domain",
        "Phylum",
        "Class",
        "Order",
        "Family",
        "Genus",
        "Species",
    ]
    for i in range(len(taxonomic_units)):
        if i == 0:  # Domain
            TaxonomicUnit.objects.create(name=taxonomic_units[i])
        else:  # Everything else
            parent = TaxonomicUnit.objects.get(name=taxonomic_units[i - 1])
            TaxonomicUnit.objects.create(name=taxonomic_units[i], parent=parent)


def print_stats(counter, start):
    print(counter)
    print("Elapsed time:")
    end = time.time()
    print(end - start)
