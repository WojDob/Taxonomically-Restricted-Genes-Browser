from django.db import models
from . import choices


class Taxon(models.Model):
    name = models.CharField(max_length=250, unique=True)
    taxonomic_unit = models.PositiveSmallIntegerField(
        null=False, blank=True, choices=choices.TAXONOMIC_UNIT
    )

    # Species related fields
    accession = models.CharField(max_length=50)
    protein_count = models.PositiveIntegerField(null=True, blank=True)
    species_isolation_index = models.FloatField(null=True, blank=True)
    genus_isolation_index = models.FloatField(null=True, blank=True)

    # Species' partial lineage for faster lookup
    family = models.ForeignKey(
        "self",related_name="f_species", null=True, on_delete=models.CASCADE)
    genus = models.ForeignKey(
        "self",related_name="g_species", null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ["taxonomic_unit"]

    def get_lineages(self):
        if self.taxonomic_unit == choices.UNIT_DOMAIN:
            lineages = self.lineages_domain.all()
        elif self.taxonomic_unit == choices.UNIT_PHYLUM:
            lineages = self.lineages_phylum.all()
        elif self.taxonomic_unit == choices.UNIT_CLASS:
            lineages = self.lineages_klass.all()
        elif self.taxonomic_unit == choices.UNIT_ORDER:
            lineages = self.lineages_order.all()
        elif self.taxonomic_unit == choices.UNIT_FAMILY:
            lineages = self.lineages_family.all()
        elif self.taxonomic_unit == choices.UNIT_GENUS:
            lineages = self.lineages_genus.all()
        elif self.taxonomic_unit == choices.UNIT_SPECIES:
            lineages = self.lineages_species.all()
        return lineages

    def get_all_species(self):
        species_ids = self.get_lineages().values_list(
            'species')
        return Taxon.objects.filter(id__in=species_ids)

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
        Taxon, related_name='lineages_domain', null=True, on_delete=models.CASCADE)
    phylum = models.ForeignKey(
        Taxon, related_name='lineages_phylum', null=True, on_delete=models.CASCADE)
    klass = models.ForeignKey(
        Taxon, related_name='lineages_klass', null=True, on_delete=models.CASCADE)
    order = models.ForeignKey(
        Taxon, related_name='lineages_order', null=True, on_delete=models.CASCADE)
    family = models.ForeignKey(
        Taxon, related_name='lineages_family', null=True, on_delete=models.CASCADE)
    genus = models.ForeignKey(
        Taxon, related_name='lineages_genus', null=True, on_delete=models.CASCADE)
    species = models.ForeignKey(
        Taxon, related_name='lineages_species', null=True, on_delete=models.CASCADE)

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
