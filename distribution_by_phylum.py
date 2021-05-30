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
        #Add each phylum as key, dict of count of 0 of every asp. as value
    #Load emboss-pfam-rbh.json to huge_dictionary
    #For asparaginase in asparaginases_list
        #for genome in huge_dictionary[asparaginase]
            #genomes_origin = origin[genome.key?]
            #phylum_count[genomes_origin] += genome.value?