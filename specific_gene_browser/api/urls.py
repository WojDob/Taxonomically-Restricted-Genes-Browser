from rest_framework.routers import DefaultRouter

from .views import GenomeViewSet, TaxonNameViewSet

router = DefaultRouter()

router.register(r"genomes", GenomeViewSet, basename="genomes")
router.register(r"taxon-names", TaxonNameViewSet, basename="taxon-names")
urlpatterns = router.urls
