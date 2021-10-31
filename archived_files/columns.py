import csv


def get_column(file, word):
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        for row in reader:
            for k, v in enumerate(row):
                if v == word:
                    return k  # immediate value return to avoid further loop iteration


search_word = "protein_count"
print(
    get_column("/home/wojdob/Desktop/masters/data/test_taxonomy_data.tsv", search_word)
)  # "data/sample.csv" is an exemplary file path


from collections import defaultdict

columns = defaultdict(list)  # each value in each column is appended to a list

with open("/home/wojdob/Desktop/masters/data/test_taxonomy_data.tsv") as f:
    reader = csv.DictReader(f, delimiter="\t")  # read rows into a dictionary format
    for row in reader:  # read a row as {column1: value1, column2: value2,...}
        for (k, v) in row.items():  # go over each column name and value
            columns[k].append(v)  # append the value into the appropriate list
            # based on column name k

print(columns["protein_count"])
