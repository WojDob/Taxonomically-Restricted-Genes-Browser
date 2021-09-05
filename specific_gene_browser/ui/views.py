from browser.models import Taxon
from django.db.models.query_utils import Q
from django.views.generic import TemplateView
from django.shortcuts import render


def home(request):
    context = dict()
    return render(request, 'ui/home.html', context)


def search_results(request):
    context = dict()
    if request.method == "POST":
        searched = request.POST.get("searched")
        results = Taxon.objects.filter(name__icontains=searched)
        context = {"searched": searched, "results": results}
        return render(request, 'ui/search_results.html', context)
    else:
        return render(request, 'ui/search_results.html', context)
