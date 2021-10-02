from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class TaxonomicUnit(models.Model):
    name = models.CharField(max_length=30, unique=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, related_name="child_taxonomic_unit"
    )

    def __str__(self):
        return self.name


class Taxon(models.Model):
    name = models.CharField(max_length=250)
    accession = models.CharField(max_length=50)
    taxonomic_unit = models.ForeignKey(
        "TaxonomicUnit", on_delete=models.CASCADE, related_name="taxons", db_index=True
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, related_name="child_taxons", db_index=True
    )

    # Genome related fields
    protein_number = models.PositiveIntegerField(null=True, blank=True)
    species_isolation_index = models.FloatField(null=True, blank=True)
    genus_isolation_index = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['taxonomic_unit']

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
    
    def __str__(self):
        return "({}) {}".format(self.taxonomic_unit.name, self.name)


class TaxonomicallyRestrictedGene(models.Model):
    accession = models.CharField(max_length=50)
    origin_genome = models.ForeignKey(
        "Taxon", on_delete=models.CASCADE, related_name="taxonomically_restricted_genes"
    )

    def __str__(self):
        return self.accession
