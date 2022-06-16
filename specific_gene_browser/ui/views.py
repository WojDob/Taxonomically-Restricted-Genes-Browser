import json

from browser import choices
from browser.models import Genome, Taxon
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView


class GeneSearchView(ListView):
    template_name = "home.html"
    model = Taxon

    def get_context_data(self, **kwargs):
        context = super(GeneSearchView, self).get_context_data(**kwargs)
        query = self.request.GET.get("q")

        context["taxon_names"] = json.dumps(
            list(Taxon.objects.all().values_list("name", flat=True))
        )
        if query:
            context["query"] = query
            try:
                searched_taxon = Taxon.objects.get(
                    name__iexact=query
                )
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
                object_list = list()
                for g in genomes:
                    object_list.append({
                        'accession': g.accession,
                        'name': g.name,
                        'family': g.lineage.family.name,
                        'genus': g.lineage.genus.name,
                        'protein_count': g.protein_count,
                        'trg_count': g.originating_trgs.count(),
                    })
                context["object_list"] = object_list
            except Taxon.DoesNotExist:
                context["object_list"] = None
        return context
