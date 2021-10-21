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
            context['query'] = query
            try:
                context["object_list"] = Taxon.objects.get(
                    name__iexact=query).get_all_species()
            except Taxon.DoesNotExist:
                context["object_list"] = None

        return context
