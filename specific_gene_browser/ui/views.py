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
                object_list = list()
                species = searched_taxon.get_all_species().select_related('family', 'genus')
                for s in species:
                    object_list.append({
                        'accession': s.accession,
                        'name': s.name,
                        'family': s.family.name,
                        'genus': s.genus.name,
                        'protein_count': s.protein_count,
                    })
                context["object_list"] = object_list
            except Taxon.DoesNotExist:
                context["object_list"] = None
        return context
