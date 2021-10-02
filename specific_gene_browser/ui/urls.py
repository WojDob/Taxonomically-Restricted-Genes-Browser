from django.urls import path

from . import views

urlpatterns = [
    path('', views.GeneSearchView.as_view(), name='home'),
]
