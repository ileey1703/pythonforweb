from django.urls import path

from .views import (
    EntrepriseCreate,
    EntrepriseDelete,
    EntrepriseDetail,
    EntrepriseList,
    EntrepriseUpdate,
)


urlpatterns = [
    path("", EntrepriseList.as_view(), name="entreprise_list"),
    path("create/", EntrepriseCreate.as_view(), name="entreprise_create"),
    path("<int:pk>/", EntrepriseDetail.as_view(), name="entreprise_detail"),
    path("<int:pk>/update/", EntrepriseUpdate.as_view(), name="entreprise_update"),
    path("<int:pk>/delete/", EntrepriseDelete.as_view(), name="entreprise_delete"),
]
