import json
import os


try:
    metadata_file = open("../data/metadata.json", "r")
except FileNotFoundError:
    print("\033[91m\n" + "No metadata file found, aborting" + "\n\033[0m")

try:
    trg_file = open("../large_data/trg.json", "r")
except FileNotFoundError:
    print("\033[91m\n" + "No trg file found, aborting" + "\n\033[0m")
metadata = json.load(metadata_file)
specific_genes_data = json.load(trg_file)

metadata_file.close()
trg_file.close()

genuses = dict()
for genome in metadata:
    gn = metadata[genome]
    genus = gn["lineage"][5]
    species = [genome, set()]
    if genus in genuses:
        genuses[genus].append(species)
    else:
        genuses[genus] = [species]


for genus in genuses:
    print(genus)
    input_file = f"../large_data/genuses/{genus}/{genus}_specific_genes.fasta"
    output_file = f"../large_data/genuses/{genus}/{genus}_clustered.fasta"
    cmd = f"cd-hit -i {input_file} -o {output_file} -M 0 -sc 1 -d 0"
    os.system(cmd)
