from django.db import models
from . import choices


class Taxon(models.Model):
    name = models.CharField(max_length=250, unique=True)
    taxonomic_unit = models.PositiveSmallIntegerField(
        null=False, blank=True, choices=choices.TAXONOMIC_UNIT
    )

    # parent = models.ForeignKey(
    #     "self",
    #     on_delete=models.CASCADE,
    #     null=True,
    #     related_name="child_taxons",
    #     db_index=True,
    # )

    # Species related fields
    accession = models.CharField(max_length=50)
    protein_count = models.PositiveIntegerField(null=True, blank=True)
    species_isolation_index = models.FloatField(null=True, blank=True)
    genus_isolation_index = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ["taxonomic_unit"]

    def get_lineages(self):
        if self.taxonomic_unit == choices.UNIT_DOMAIN:
            lineages = self.domain.all()
        elif self.taxonomic_unit == choices.UNIT_PHYLUM:
            lineages = self.phylum.all()
        elif self.taxonomic_unit == choices.UNIT_CLASS:
            lineages = self.klass.all()
        elif self.taxonomic_unit == choices.UNIT_ORDER:
            lineages = self.order.all()
        elif self.taxonomic_unit == choices.UNIT_FAMILY:
            lineages = self.family.all()
        elif self.taxonomic_unit == choices.UNIT_GENUS:
            lineages = self.genus.all()
        elif self.taxonomic_unit == choices.UNIT_SPECIES:
            lineages = self.species.all()
        return lineages

    def get_all_species(self):
        species_ids = self.get_lineages().values_list(
            'species')
        return list(Taxon.objects.filter(id__in=species_ids))

    def get_higher_taxon(self, taxon_name):
        classification = self.get_classification()
        for taxon in classification:
            if taxon.get_taxonomic_unit_display().lower() == taxon_name.lower():
                return taxon

    def print_classification(self):
        self.get_lineages().first().print_classification(self.taxonomic_unit)

    def get_classification(self):
        return self.get_lineages().first().get_classification(self.taxonomic_unit)

    def __str__(self):
        return "({}) {}".format(self.get_taxonomic_unit_display(), self.name)


class Lineage(models.Model):
    domain = models.ForeignKey(
        Taxon, related_name='domain', null=True, on_delete=models.CASCADE)
    phylum = models.ForeignKey(
        Taxon, related_name='phylum', null=True, on_delete=models.CASCADE)
    klass = models.ForeignKey(
        Taxon, related_name='klass', null=True, on_delete=models.CASCADE)
    order = models.ForeignKey(
        Taxon, related_name='order', null=True, on_delete=models.CASCADE)
    family = models.ForeignKey(
        Taxon, related_name='family', null=True, on_delete=models.CASCADE)
    genus = models.ForeignKey(
        Taxon, related_name='genus', null=True, on_delete=models.CASCADE)
    species = models.OneToOneField(
        Taxon, related_name='species', on_delete=models.CASCADE)

    def get_model_fields(self):
        return [f.name for f in self._meta.get_fields() if f.name != "id"]

    def print_classification(self, limit=6):
        fields = self.get_model_fields()
        for count, field in enumerate(fields):
            print(f"{getattr(self, field)}")
            if count == limit:
                break

    def get_classification(self, limit=6):
        fields = self.get_model_fields()
        classification = list()
        for count, field in enumerate(fields):
            classification.append(getattr(self, field))
            if count == limit:
                break

        return classification

    def get_field(self, field_name):
        if field_name in self.get_model_fields():
            return getattr(self, field_name)


class TaxonomicallyRestrictedGene(models.Model):
    accession = models.CharField(max_length=50)
    origin_genome = models.ForeignKey(
        "Taxon", on_delete=models.CASCADE, related_name="taxonomically_restricted_genes"
    )

    def __str__(self):
        return self.accession
