# from django_filters import rest_framework as rf_filters
# from browser.models import TaxonomicallyRestrictedGene
# from django.db.models import Q


# class TaxonomicallyRestrictedGeneFilter(rf_filters.FilterSet):
#     genus = rf_filters.CharFilter(method="genus_specific_filter")
#     species = rf_filters.CharFilter(method="species_specific_filter")

#     class Meta:
#         model = TaxonomicallyRestrictedGene
#         fields = {"accession": ["icontains"]}

#     def genus_specific_filter(self, queryset, name, value):
#         return queryset.filter(
#             Q(specific_to__taxonomic_unit=5) | Q(specific_to__name__icontains=value)
#         )

#     def species_specific_filter(self, queryset, name, value):
#         return queryset.filter(
#             Q(specific_to__taxonomic_unit=6) | Q(specific_to__name__icontains=value)
#         )
