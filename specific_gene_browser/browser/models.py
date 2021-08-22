from django.db import models


class TaxonomicUnit(models.Model):
    name = models.CharField(max_length=30, unique=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, related_name="child_taxonomic_unit"
    )

    def __str__(self):
        return self.name


class Taxon(models.Model):
    name = models.CharField(max_length=250)
    taxonomic_unit = models.ForeignKey(
        "TaxonomicUnit", on_delete=models.CASCADE, related_name="taxons", db_index=True
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, related_name="child_taxons", db_index=True
    )

    def __str__(self):
        return "({}) {}".format(self.taxonomic_unit.name,self.name)

    def print_whole_classification(self):
        parent = self
        while parent:
            print("{}\t{}".format(parent.taxonomic_unit.name, parent.name))
            parent = parent.parent

    def get_whole_classification(self):
        classification_list = list()
        parent = self
        while parent:
            classification_list.append(parent)
            parent = parent.parent
        return classification_list


class SpecificGene(models.Model):
    name = models.CharField(max_length=250)
    specific_to = models.ForeignKey(
        "Taxon", on_delete=models.CASCADE, related_name="specific_genes"
    )

    def __str__(self):
        return self.name
