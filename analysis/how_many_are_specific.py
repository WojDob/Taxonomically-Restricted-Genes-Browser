"""
CREATED: 2021-12-22
What % of all proteins are specific (separately species and genus)
How many specific genes are there 
  on average
  min
  max
  standard deviation
  histogram
  quartiles
For each species:
  how many genes are specific - both count and percentage
  top 10
  bottom 10
"""
import json


try:
    metadata_file = open("../data/metadata.json","r")
except FileNotFoundError:
    print("\033[91m\n" + "No metadata file found, aborting" + "\n\033[0m")

try:
    trg_file = open("../large_data/trg.json","r")
except FileNotFoundError:
    print("\033[91m\n" + "No trg file found, aborting" + "\n\033[0m")


metadata = json.load(metadata_file)
specific_genes_data = json.load(trg_file)    

metadata_file.close()
trg_file.close()

print(len(metadata))
print(len(specific_genes_data))