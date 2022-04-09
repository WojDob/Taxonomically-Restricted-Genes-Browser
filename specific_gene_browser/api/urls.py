from rest_framework.routers import DefaultRouter

from .views import GenomeViewSet, TaxonViewSet, TaxonomicallyRestrictedGeneViewset

router = DefaultRouter()

router.register(r"genomes", GenomeViewSet, basename="genomes")
router.register(r"taxons", TaxonViewSet, basename="taxons")
router.register(r"trgs", TaxonomicallyRestrictedGeneViewset, basename="trgs")

urlpatterns = router.urls
