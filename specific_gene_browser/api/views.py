from browser import choices
from browser.models import Genome, Taxon, TaxonomicallyRestrictedGene
from django.shortcuts import get_list_or_404, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import (
    GenomeListSerializer,
    GenomeDetailSerializer,
    TaxonListSerializer,
    TaxonDetailSerializer,
    TaxonomicallyRestrictedGeneDetailSerializer,
    TaxonomicallyRestrictedGeneListSerializer,
)


class GenomeViewSet(viewsets.ReadOnlyModelViewSet):
    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request):
        queryset = self.get_queryset()
        serializer = GenomeListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(Genome, pk=pk)
        serializer = GenomeDetailSerializer(item)
        return Response(serializer.data)

    def get_queryset(self):
        query = self.request.GET.get("q", None)
        if query:
            searched_taxon = get_list_or_404(Taxon, name__iexact=query)[0]
            taxonomic_unit = searched_taxon.taxonomic_unit
            if taxonomic_unit == choices.UNIT_DOMAIN:
                genomes = Genome.objects.filter(
                    lineage__domain=searched_taxon
                ).select_related("lineage__family", "lineage__genus")
            if taxonomic_unit == choices.UNIT_PHYLUM:
                genomes = Genome.objects.filter(
                    lineage__phylum=searched_taxon
                ).select_related("lineage__family", "lineage__genus")
            if taxonomic_unit == choices.UNIT_CLASS:
                genomes = Genome.objects.filter(
                    lineage__klass=searched_taxon
                ).select_related("lineage__family", "lineage__genus")
            if taxonomic_unit == choices.UNIT_ORDER:
                genomes = Genome.objects.filter(
                    lineage__order=searched_taxon
                ).select_related("lineage__family", "lineage__genus")
            if taxonomic_unit == choices.UNIT_FAMILY:
                genomes = Genome.objects.filter(
                    lineage__family=searched_taxon
                ).select_related("lineage__family", "lineage__genus")
            if taxonomic_unit == choices.UNIT_GENUS:
                genomes = Genome.objects.filter(
                    lineage__genus=searched_taxon
                ).select_related("lineage__family", "lineage__genus")
            if taxonomic_unit == choices.UNIT_SPECIES:
                genomes = Genome.objects.filter(
                    lineage__species=searched_taxon
                ).select_related("lineage__family", "lineage__genus")
        else:
            genomes = []
        return genomes


class TaxonViewSet(viewsets.ReadOnlyModelViewSet):
    def list(self, request):
        queryset = self.get_queryset()
        serializer = TaxonListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(Taxon, pk=pk)
        serializer = TaxonDetailSerializer(item)
        return Response(serializer.data)

    def get_queryset(self):
        query = self.request.GET.get("q", None)
        if query:
            taxons = Taxon.objects.filter(name__icontains=query).prefetch_related(
                "taxonomically_restricted_genes"
            )
        else:
            taxons = []
        return taxons


class TaxonomicallyRestrictedGeneViewset(viewsets.ReadOnlyModelViewSet):
    def list(self, request):
        queryset = self.get_queryset()
        serializer = TaxonomicallyRestrictedGeneListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(TaxonomicallyRestrictedGene, pk=pk)
        serializer = TaxonomicallyRestrictedGeneDetailSerializer(item)
        return Response(serializer.data)

    def get_queryset(self):
        query = self.request.GET.get("q", None)
        if query:
            trgs = TaxonomicallyRestrictedGene.objects.filter(
                accession__icontains=query
            ).prefetch_related("specific_to")
        else:
            trgs = []
        return trgs
