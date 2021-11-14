import csv
import os
import time
from pprint import pprint

from browser import choices
from browser.models import Genome, Lineage, Taxon
from django.conf import settings
from django.db import transaction

"""
To run: 
    ./manage.py runscript load_taxonomy --script-args ~/Downloads/bac120_metadata_r202.tsv

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
####################################################################################
    print("Creating taxons")
    start = time.time()
    to_create = list()
    for row in read_tsv:
        gtdb_representative = row[15]
        if gtdb_representative == "t":
            tree = row[16].split(";")
            for i in range(len(tree)):
                to_create.append(Taxon(
                    name=tree[i][3:],
                    taxonomic_unit=taxonomy_symbols[tree[i][0]],
                ))
    tsv_file.close()
    print(f"Bulk creating {len(to_create)} objects...")
    Taxon.objects.bulk_create(to_create, ignore_conflicts=True)
    print_stats(start)
####################################################################################
    print("Creating lineages")
    tsv_file = open(filepath)
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    next(read_tsv)  # Skip the first 'title' row.

    start = time.time()
    to_create = list()
    for row in read_tsv:
        gtdb_representative = row[15]
        if gtdb_representative == "t":
            tree = row[16].split(";")
            lineage = Lineage()
            for i in range(len(tree)):
                if i == 0:
                    lineage.domain = Taxon.objects.get(
                        name=tree[i][3:], taxonomic_unit=choices.UNIT_DOMAIN)
                elif i == 1:
                    lineage.phylum = Taxon.objects.get(
                        name=tree[i][3:], taxonomic_unit=choices.UNIT_PHYLUM)
                elif i == 2:
                    lineage.klass = Taxon.objects.get(
                        name=tree[i][3:], taxonomic_unit=choices.UNIT_CLASS)
                elif i == 3:
                    lineage.order = Taxon.objects.get(
                        name=tree[i][3:], taxonomic_unit=choices.UNIT_ORDER)
                elif i == 4:
                    lineage.family = Taxon.objects.get(
                        name=tree[i][3:], taxonomic_unit=choices.UNIT_FAMILY)
                elif i == 5:
                    lineage.genus = Taxon.objects.get(
                        name=tree[i][3:], taxonomic_unit=choices.UNIT_GENUS)
                elif i == 6:
                    lineage.species = Taxon.objects.get(
                        name=tree[i][3:], taxonomic_unit=choices.UNIT_SPECIES)
            to_create.append(lineage)
    tsv_file.close()
    print(f"Bulk creating {len(to_create)} objects...")
    Lineage.objects.bulk_create(to_create, ignore_conflicts=True)
    print_stats(start)
####################################################################################
    print("Creating genomes")
    tsv_file = open(filepath)
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    next(read_tsv)  # Skip the first 'title' row.
    start = time.time()
    to_create = list()
    for row in read_tsv:
        gtdb_representative = row[15]
        if gtdb_representative == "t":
            tree = row[16].split(";")
            protein_count = row[88]
            accession = row[0]
            name = tree[-1][3:]
            to_create.append(Genome(
                name=name,
                protein_count=protein_count,
                accession=accession,
                lineage=Lineage.objects.get(species__name=name)
            ))
    tsv_file.close()
    print(f"Bulk creating {len(to_create)} objects...")
    Genome.objects.bulk_create(to_create, ignore_conflicts=True)
    print_stats(start)
####################################################################################


def check_if_taxons_are_loaded():
    if Taxon.objects.count() > 0:
        print("\033[91m\n" + "Taxons in database, aborting" + "\n\033[0m")
        exit()


def print_stats(start):
    print("Elapsed time:")
    end = time.time()
    print(end - start)
