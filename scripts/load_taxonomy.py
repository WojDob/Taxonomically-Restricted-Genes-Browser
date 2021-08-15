"""
CREATED: 14.08.2021

"""
import csv
from pprint import pprint
tsv_file = open("data/test_data.tsv")

read_tsv = csv.reader(tsv_file, delimiter="\t")

taxonomy_symbols = {
    "d":"Domain",
    "p":"Phylum",
    "c":"Class",
    "o":"Order",
    "f":"Family",
    "g":"Genus",
    "s":"Species",
}
for row in read_tsv:

    for tax in row[16].split(";"):
        print("{}    {}".format(taxonomy_symbols[tax[0]], tax[3:]))
    print()
tsv_file.close()