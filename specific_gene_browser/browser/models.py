from django.db import models
from . import choices


class Taxon(models.Model):
    name = models.CharField(max_length=250)
    taxonomic_unit = models.PositiveSmallIntegerField(
        null=False, blank=True, choices=choices.TAXONOMIC_UNIT
    )

    class Meta:
        unique_together = (
            "name",
            "taxonomic_unit",
        )

    def __str__(self):
        return "({}) {}".format(self.get_taxonomic_unit_display(), self.name)


class Lineage(models.Model):
    domain = models.ForeignKey(
        Taxon, related_name="lineages_domain", null=True, on_delete=models.CASCADE
    )
    phylum = models.ForeignKey(
        Taxon, related_name="lineages_phylum", null=True, on_delete=models.CASCADE
    )
    klass = models.ForeignKey(
        Taxon, related_name="lineages_klass", null=True, on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        Taxon, related_name="lineages_order", null=True, on_delete=models.CASCADE
    )
    family = models.ForeignKey(
        Taxon, related_name="lineages_family", null=True, on_delete=models.CASCADE
    )
    genus = models.ForeignKey(
        Taxon, related_name="lineages_genus", null=True, on_delete=models.CASCADE
    )
    species = models.ForeignKey(
        Taxon, related_name="lineages_species", null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return "{}".format(self.species.name)


class Genome(models.Model):
    accession = models.CharField(max_length=50)
    name = models.CharField(max_length=250)
    protein_count = models.PositiveIntegerField(null=True, blank=True)
    species_isolation_index = models.FloatField(null=True, blank=True)
    genus_isolation_index = models.FloatField(null=True, blank=True)
    lineage = models.ForeignKey(Lineage, on_delete=models.CASCADE)


class TaxonomicallyRestrictedGene(models.Model):
    accession = models.CharField(max_length=50)
    origin_genome = models.ForeignKey(
        "Genome", on_delete=models.CASCADE, related_name="originating_trgs"
    )
    specific_to = models.ForeignKey(
        "Taxon", on_delete=models.CASCADE, related_name="taxonomically_restricted_genes"
    )
    length = models.PositiveIntegerField(null=True, blank=True)
    entropy = models.FloatField(null=True, blank=True)
    disorder = models.FloatField(null=True, blank=True)
    aggregation = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.accession

    @property
    def type(self):
        return f"{self.specific_to.get_taxonomic_unit_display()} specific"
