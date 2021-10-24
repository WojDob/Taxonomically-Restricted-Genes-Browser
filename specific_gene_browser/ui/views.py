import json

from browser.models import Taxon
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView


class GeneSearchView(ListView):
    template_name = 'home.html'
    model = Taxon

    def get_context_data(self, **kwargs):
        context = super(GeneSearchView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')

        context['taxon_names'] = json.dumps(
            list(Taxon.objects.all().values_list('name', flat=True)))
        if query:
            context['query'] = query
            try:
                context["object_list"] = Taxon.objects.get(
                    name__iexact=query).get_all_species()
            except Taxon.DoesNotExist:
                context["object_list"] = None
        return context
