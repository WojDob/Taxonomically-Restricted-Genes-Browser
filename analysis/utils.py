import json

def get_genuses():
    metadata = get_metadata()
    genuses = set()
    for genome in metadata:
        gn = metadata[genome]
        genus = gn["lineage"][5]
        genuses.add(genus)
    return genuses

def get_metadata():
    try:
        metadata_file = open("../data/metadata.json", "r")
    except FileNotFoundError:
        print("\033[91m\n" + "No metadata file found, aborting" + "\n\033[0m")
    metadata = json.load(metadata_file)
    metadata_file.close()
    return metadata