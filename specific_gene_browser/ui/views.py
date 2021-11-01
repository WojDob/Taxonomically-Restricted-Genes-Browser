import json

from browser import choices
from browser.models import Taxon
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
                if searched_taxon.taxonomic_unit == choices.UNIT_DOMAIN:
                    species_ids = searched_taxon.domain.all().values_list(
                        'species')
                elif searched_taxon.taxonomic_unit == choices.UNIT_PHYLUM:
                    species_ids = searched_taxon.phylum.all().values_list(
                        'species')
                elif searched_taxon.taxonomic_unit == choices.UNIT_CLASS:
                    species_ids = searched_taxon.klass.all().values_list(
                        'species')
                elif searched_taxon.taxonomic_unit == choices.UNIT_ORDER:
                    species_ids = searched_taxon.order.all().values_list(
                        'species')
                elif searched_taxon.taxonomic_unit == choices.UNIT_FAMILY:
                    species_ids = searched_taxon.family.all().values_list(
                        'species')
                elif searched_taxon.taxonomic_unit == choices.UNIT_GENUS:
                    species_ids = searched_taxon.genus.all().values_list(
                        'species')
                elif searched_taxon.taxonomic_unit == choices.UNIT_SPECIES:
                    species_ids = searched_taxon.species.all().values_list(
                        'species')
                context["object_list"] = list(Taxon.objects.filter(id__in=species_ids))
            except Taxon.DoesNotExist:
                context["object_list"] = None
        return context
