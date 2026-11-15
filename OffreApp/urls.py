from django.urls import path

from .views import OffreCreate, OffreDelete, OffreDetail, OffreList, OffreUpdate


urlpatterns = [
    path("", OffreList.as_view(), name="offre_list"),
    path("create/", OffreCreate.as_view(), name="offre_create"),
    path("<int:pk>/", OffreDetail.as_view(), name="offre_detail"),
    path("<int:pk>/update/", OffreUpdate.as_view(), name="offre_update"),
    path("<int:pk>/delete/", OffreDelete.as_view(), name="offre_delete"),
]
