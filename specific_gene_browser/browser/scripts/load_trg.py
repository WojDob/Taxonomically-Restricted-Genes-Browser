import json

from browser.models import Genome, Taxon, TaxonomicallyRestrictedGene


"""
To run: 
    manage.py runscript load_trg --script-args large_data/all_specific_genes_stats_full.json

"""


def run(*args):

    check_if_taxons_are_loaded()
    taxon_names_to_ids = find_taxons()
    genome_names_to_ids = find_genomes()
    print("Loading file")
    with open(args[0]) as f:
        all_specific_genes_stats = json.load(f)

    to_create = list()
    print("Parsing stats")
    for key in all_specific_genes_stats:
        record = all_specific_genes_stats[key]
        if not record["genus_specific_to"]:
            specific_to = taxon_names_to_ids[record["origin_species_name"]]
        else:
            specific_to = taxon_names_to_ids[record["genus_specific_to"]]
        to_create.append(
            TaxonomicallyRestrictedGene(
                accession=record["accession"],
                origin_genome=genome_names_to_ids[record["origin"]],
                specific_to=specific_to,
                length=record["length"],
                entropy=record["shannon"],
                disorder=record["disorder"],
                aggregation=record["aggregation"],
            )
        )
    print(f"Bulk creating {len(to_create)} objects...")
    TaxonomicallyRestrictedGene.objects.bulk_create(to_create, ignore_conflicts=True)


def check_if_taxons_are_loaded():
    if Taxon.objects.count() == 0:
        print("\033[91m\n" + "No taxons in database" + "\n\033[0m")
        exit()


def find_taxons():
    taxon_ids = dict()
    for taxon in Taxon.objects.all():
        taxon_ids[taxon.name] = taxon
    return taxon_ids


def find_genomes():
    genome_ids = dict()
    for genome in Genome.objects.all():
        genome_ids[genome.accession] = genome
    return genome_ids
