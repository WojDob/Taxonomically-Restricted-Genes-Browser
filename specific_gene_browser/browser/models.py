from django.db import models
from . import choices


class Taxon(models.Model):
    name = models.CharField(max_length=250)
    accession = models.CharField(max_length=50)
    taxonomic_unit = models.PositiveSmallIntegerField(
        null=False,
        blank=True,
        choices=choices.TAXONOMIC_UNIT,
    )

    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, related_name="child_taxons", db_index=True
    )

    # Genome related fields
    protein_count = models.PositiveIntegerField(null=True, blank=True)
    species_isolation_index = models.FloatField(null=True, blank=True)
    genus_isolation_index = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['taxonomic_unit']

    def print_whole_classification(self):
        parent = self
        while parent:
            print("{}\t{}".format(parent.get_taxonomic_unit_display(), parent.name))
            parent = parent.parent

    def get_whole_classification(self):
        classification_list = list()
        parent = self
        while parent:
            classification_list.append(parent)
            parent = parent.parent
        return classification_list

    def get_all_species(self):
        return list(self.search_for_species())

    def search_for_species(self):
        if not self.child_taxons.all():
            yield self

        for child in self.child_taxons.all():
            for leaf in child.search_for_species():
                yield leaf
    
    def __str__(self):
        return "({}) {}".format(self.get_taxonomic_unit_display(), self.name)


class TaxonomicallyRestrictedGene(models.Model):
    accession = models.CharField(max_length=50)
    origin_genome = models.ForeignKey(
        "Taxon", on_delete=models.CASCADE, related_name="taxonomically_restricted_genes"
    )

    def __str__(self):
        return self.accession
