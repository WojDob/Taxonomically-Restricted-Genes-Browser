"""
CREATED: 
    2021-05-29


USAGE:
    Count how many of each of 5 asparaginase proteins are in each bacteria phylum

    Example goal output:
                        EcaI    EcaII   EcaIII  ReAIV   ReAV
    Proteobacteria      30      5       6       1       0
    Bacteroidota        2       1       4       1       2
    ...


USED DATA FILES:
    data/metadata.json
    Contains data about classification of each bacteria 

    data/emboss-pfam-rbh.json
    Result of earlier analysis, contains data about orthologs of asparaginases from each genome
"""

import json
from pprint import pprint

ASPARAGINASES = ["ReAV", "ReAIV", "EcAI", "EcAII", "EcAIII"]


# EXTRACT PHYLUMS

with open("data/metadata.json", "r") as json_file:
    metadata = json.load(json_file)

phylums = set()
origin_of_genomes = dict()

for genome in metadata:
    phylum = metadata[genome]["lineage"][1]
    phylums.add(phylum)
    origin_of_genomes[genome] = phylum


# COUNT NUMBER OF ORTHOLOGS FOR EACH PHYLUM

phylum_count = dict()
phylum_count_strict = dict()
for phylum in phylums:
    phylum_count[phylum] = {"ReAV": 0, "ReAIV": 0, "EcAI": 0, "EcAII": 0, "EcAIII": 0}
    phylum_count_strict[phylum] = {
        "ReAV": 0,
        "ReAIV": 0,
        "EcAI": 0,
        "EcAII": 0,
        "EcAIII": 0,
    }


with open("data/emboss-pfam-rbh.json", "r") as json_file:
    orthologs_data = json.load(json_file)

for asparaginase in ASPARAGINASES:
    for genome in orthologs_data[asparaginase]:
        genomes_origin = origin_of_genomes[genome]
        phylum_count[genomes_origin][asparaginase] += len(
            orthologs_data[asparaginase][genome]
        )
        # strict counting
        for ortholog in orthologs_data[asparaginase][genome]:
            if (
                orthologs_data[asparaginase][genome][ortholog]["pfam"] == 1
                or orthologs_data[asparaginase][genome][ortholog]["query_coverage"]
                >= 50
            ):
                phylum_count_strict[genomes_origin][asparaginase] += 1


# SAVE AND RETURN DATA
with open("data/phylum_count.json", "w") as f:
    json.dump(phylum_count, f, indent=4)
with open("data/phylum_count_strict.json", "w") as f:
    json.dump(phylum_count_strict, f, indent=4)


def print_table(count_dictionary):
    print("\t\t\tReAV\tReAIV\tEcAI\tEcAII\tEcAIII")
    for phylum in phylums:
        print(
            "{:<24}{:<8}{:<8}{:<8}{:<8}{:<8}".format(
                phylum,
                count_dictionary[phylum]["ReAV"],
                count_dictionary[phylum]["ReAIV"],
                count_dictionary[phylum]["EcAI"],
                count_dictionary[phylum]["EcAII"],
                count_dictionary[phylum]["EcAIII"],
            )
        )


print_table(phylum_count)
print("pfam==1 or query_coverage>=50")
print_table(phylum_count_strict)
