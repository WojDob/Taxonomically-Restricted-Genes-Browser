# Taxonomically Restricted Genes (TRG) Analysis and API
This repository contains the code used in a data analysis project that identified and analyzed taxonomically restricted genes (TRGs) in bacteria. The project also includes a REST API that allows users to browse the data collected during the project. The work was part of a master's thesis.

## Project Overview
The project aimed to identify and analyze TRGs in bacteria. TRGs are a group of genes that occur only within a single taxon and play a crucial role in the evolution of unique features that distinguish different organism lineages. For example, they are responsible for encoding the topoisomerase V protein, which, due to its unique stability at high temperatures, is used in sequencing kits.

The project analyzed sequences from 45,555 bacterial genomes and identified 6,788,867 TRGs, including 4,150,013 species-specific and 2,638,854 genus-specific. The percentage of TRGs in bacterial taxa is positively correlated (p < 10-4) with the degree of phylogenetic isolation of a given taxon.

## Repository Contents
This repository contains all the code used for the analysis and the construction of the REST API. The main components are:

- **Data Analysis Notebooks:** These Jupyter Notebooks were used to identify and analyze the TRGs from the bacterial genomes. They are available in the `analysis` directory.

- **Django REST API:** The API allows users to browse the calculated parameters for each of the identified taxonomically specific genes. You can find it in the `specific_gene_browser` directory.

### Using the REST API
The REST API allows users to quickly retrieve detailed data obtained from the analysis of TRGs. Users can submit a query containing the name or part of the name of the bacterial taxon of interest to get information about its taxonomic unit and the number of TRGs found within it.

Users can also submit a query by providing the name or identifier of a specific bacterial genome to get taxonomy data for the indicated genome, its total number of proteins, and a list of TRGs found in that genome. The specific_to field indicates the genus or species to which the TRG is specific.

Finally, users can submit a query using the identifier of a specific TRG to get information about which genome it comes from, the taxonomic level for which it is specific, the accession number, and the parameters calculated during the analysis.

## Results
This project successfully identified 6,788,867 TRGs, including 4,150,013 species-specific and 2,638,854 genus-specific. The TRGs were grouped based on 90% sequence identity, resulting in 2,118,544 TRG families. Only 1.7% of TRG proteins were found to have at least one protein domain. All protein domains found were in genus-specific TRG proteins.

### Requirements
The requirements for running the scripts and the API are listed in the requirements.txt file. Please install them before running the code.
