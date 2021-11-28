from browser import choices
from browser.models import Genome, Taxon
from django.shortcuts import get_list_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import GenomeSerializer, TaxonSerializer


class GenomeViewSet(viewsets.ReadOnlyModelViewSet):

    @method_decorator(cache_page(60*60*2))
    def list(self, request):
        queryset = self.get_queryset()
        serializer = GenomeSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query:
            searched_taxon = get_list_or_404(Taxon, name__iexact=query)[0]
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
        else:
            genomes = Genome.objects.all()
        return genomes


class TaxonNameViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaxonSerializer

    def list(self, request):
        return Response(self.get_queryset().values_list("name", flat=True))

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query:
            taxons_containing_query = Taxon.objects.filter(
                name__icontains=query)
        else:
            taxons_containing_query = Taxon.objects.all()
        return taxons_containing_query
