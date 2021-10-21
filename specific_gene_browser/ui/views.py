from browser.models import Taxon
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404


class GeneSearchView(ListView):
    template_name = 'ui/home.html'
    model = Taxon


    def get_context_data(self, **kwargs):
        context = super(GeneSearchView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')

        if query:
            context['query'] = self.request.GET.get('q')
            # TODO: allow searching higher taxons
            species_taxonomic_unit = 6
            object_list = self.model.objects.filter(
                name__icontains=query, taxonomic_unit=species_taxonomic_unit)
        else:
            object_list = self.model.objects.none()
        context["object_list"] = object_list
        return context
