"""
03.02.21
"""
import json
from Bio import SeqIO

try:
    trg_file = open("../large_data/trg.json", "r")
except FileNotFoundError:
    print("\033[91m\n" + "No trg file found, aborting" + "\n\033[0m")
specific_genes_data = json.load(trg_file)

trg_file.close()


all_genus_specific = dict()
for genome in specific_genes_data:
    all_genus_specific[genome] = set()
    for gene in specific_genes_data[genome]:
        if gene[1] == 0:
            all_genus_specific[genome].add(gene[0])



output_file = "genus_specific_genes.fasta"
with open("genus_specific_genes.fasta", "a") as handle:
    for genome in all_genus_specific:
        wanted = all_genus_specific[genome]
        input_file = f"../large_data/protein_faa_reps/bacteria/{genome}_protein.faa"
        records = (r for r in SeqIO.parse(input_file, "fasta") if r.id in wanted)
        count = SeqIO.write(records, handle, "fasta")
        if count < len(wanted):
            print("Warning %i IDs not found in %s" % (len(wanted) - count, input_file))
