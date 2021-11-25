from rest_framework.routers import DefaultRouter
from .views import GenomeViewSet

router = DefaultRouter()

router.register(r"genomes", GenomeViewSet, basename="genomes")

urlpatterns = router.urls
