from rest_framework.routers import DefaultRouter

from .views import GenomeViewSet, TaxonNameViewSet

router = DefaultRouter()

router.register(r"genomes", GenomeViewSet, basename="genomes")
router.register(r"taxons", TaxonNameViewSet, basename="taxons")
urlpatterns = router.urls
