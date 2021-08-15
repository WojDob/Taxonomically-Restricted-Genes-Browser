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
        "TaxonomicUnit", on_delete=models.CASCADE, related_name="taxons"
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, related_name="child_taxons"
    )

    def __str__(self):
        return self.name


class SpecificGene(models.Model):
    name = models.CharField(max_length=250)
    specific_to = models.ForeignKey(
        "Taxon", on_delete=models.CASCADE, related_name="specific_genes"
    )

    def __str__(self):
        return self.name
