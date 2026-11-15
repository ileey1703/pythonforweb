from django.urls import path

from .views import (
    VehiculeCreate,
    VehiculeDelete,
    VehiculeDetail,
    VehiculeList,
    VehiculeUpdate,
)


urlpatterns = [
    path("", VehiculeList.as_view(), name="vehicule_list"),
    path("create/", VehiculeCreate.as_view(), name="vehicule_create"),
    path("<int:pk>/", VehiculeDetail.as_view(), name="vehicule_detail"),
    path("<int:pk>/update/", VehiculeUpdate.as_view(), name="vehicule_update"),
    path("<int:pk>/delete/", VehiculeDelete.as_view(), name="vehicule_delete"),
]
