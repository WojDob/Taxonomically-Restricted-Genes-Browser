"""
CREATED: 
    2021-05-31


USAGE:
    Count how many of each differnt phylums, families etc. of bacteria there are
    The end result should return about 30 thousand different species'


USED DATA FILES:
    data/metadata.json
    Contains data about classification of each bacteria 

"""
import json
from pprint import pprint
from config import TAX_LEVELS


tax_levels_count = dict()

for lvl in TAX_LEVELS:
    tax_levels_count[lvl] = set()

with open("data/metadata.json", "r") as json_file:
    metadata = json.load(json_file)

for genome in metadata:
    for i in range(7):
        tax_levels_count[TAX_LEVELS[i]].add(metadata[genome]["lineage"][i])

for key in tax_levels_count:
    tax_levels_count[key] = len(tax_levels_count[key])

with open("data/taxonomy_count.json", "w") as f:
    json.dump(tax_levels_count, f, indent=4)
