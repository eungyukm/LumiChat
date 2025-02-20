from django.urls import path
from .views import SearchLocationView, LocationDetailView

urlpatterns = [
    path("search/", SearchLocationView.as_view(), name="search_location"),
    path("location/<str:id>/", LocationDetailView.as_view(), name="location_detail"),
]
