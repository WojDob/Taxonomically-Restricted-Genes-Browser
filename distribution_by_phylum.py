'''
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
'''

import json
from pprint import pprint

ASPARAGINASES = ['ReAV','ReAIV','EcAI','EcAII','EcAIII']


#Extract phylums
with open('data/metadata.json','r') as json_file:
    metadata = json.load(json_file)

phylums = set()
origin_of_genomes = dict()

for genome in metadata:
    phylum = metadata[genome]["lineage"][1]
    phylums.add(phylum)
    origin_of_genomes[genome] = phylum


#Count number of orthologs of each asp. for each phylum
    #Create phylum_count dict
phylum_count = dict()
        #Add each phylum as key, dict of count of 0 of every asp. as value
for phylum in phylums:
    phylum_count[phylum] = {
        'ReAV':0,
        'ReAIV':0,
        'EcAI':0,
        'EcAII':0,
        'EcAIII':0,
    }

    #Load emboss-pfam-rbh.json to huge_dictionary
with open('data/emboss-pfam-rbh.json','r') as json_file:
    orthologs_data = json.load(json_file)

for asparaginase in ASPARAGINASES:
    for genome in orthologs_data[asparaginase]:
        genomes_origin = origin_of_genomes[genome]
        phylum_count[genomes_origin][asparaginase] += len(orthologs_data[asparaginase][genome])


with open('data/phylum_distribution.json', 'w') as f:
    json.dump(phylum_count, f, indent=4)