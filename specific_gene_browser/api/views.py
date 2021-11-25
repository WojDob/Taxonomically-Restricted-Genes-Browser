from django.shortcuts import get_list_or_404
from rest_framework import mixins, viewsets
from browser.models import Taxon, Genome
from browser import choices
from .serializers import GenomeSerializer

class GenomeViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    serializer_class = GenomeSerializer

    def get_queryset(self):
        searched_taxon = get_list_or_404(Taxon, name__iexact=self.request.GET.get('query', None))[0]
        taxonomic_unit = searched_taxon.taxonomic_unit
        if taxonomic_unit == choices.UNIT_DOMAIN:
            genomes = Genome.objects.filter(lineage__domain=searched_taxon).select_related(
                'lineage__family', 'lineage__genus')
        if taxonomic_unit == choices.UNIT_PHYLUM:
            genomes = Genome.objects.filter(lineage__phylum=searched_taxon).select_related(
                'lineage__family', 'lineage__genus')
        if taxonomic_unit == choices.UNIT_CLASS:
            genomes = Genome.objects.filter(lineage__klass=searched_taxon).select_related(
                'lineage__family', 'lineage__genus')
        if taxonomic_unit == choices.UNIT_ORDER:
            genomes = Genome.objects.filter(lineage__order=searched_taxon).select_related(
                'lineage__family', 'lineage__genus')
        if taxonomic_unit == choices.UNIT_FAMILY:
            genomes = Genome.objects.filter(lineage__family=searched_taxon).select_related(
                'lineage__family', 'lineage__genus')
        if taxonomic_unit == choices.UNIT_GENUS:
            genomes = Genome.objects.filter(lineage__genus=searched_taxon).select_related(
                'lineage__family', 'lineage__genus')
        if taxonomic_unit == choices.UNIT_SPECIES:
            genomes = Genome.objects.filter(lineage__species=searched_taxon).select_related(
                'lineage__family', 'lineage__genus')
        return genomes
