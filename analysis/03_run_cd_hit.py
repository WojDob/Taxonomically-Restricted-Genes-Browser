import json
import os

try:
    metadata_file = open("../data/metadata.json", "r")
except FileNotFoundError:
    print("\033[91m\n" + "No metadata file found, aborting" + "\n\033[0m")

metadata = json.load(metadata_file)

metadata_file.close()

genuses = set()
for genome in metadata:
    gn = metadata[genome]
    genus = gn["lineage"][5]
    genuses.add(genus)

for genus in genuses:
    input_file = f"../large_data/genuses/{genus}/{genus}_specific_genes.fasta"
    output_file = f"../large_data/genuses/{genus}/{genus}_clustered.fasta"
    cmd = f"cd-hit -i {input_file} -o {output_file} -M 0 -sc 1 -d 0"
    os.system(cmd)
