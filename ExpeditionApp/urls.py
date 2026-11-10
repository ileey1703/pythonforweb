from .views import *
from django.urls import path


urlpatterns =[
    path('home/', home, name='home'),
    path('w/<str:name>' , welcome, name="welcomeFunction"),
    path('list/', listExpedition , name="list"),
    path('detail/<int:pk>/', detailExpedition, name="detail"),
    path('delete/<int:pk>/', deleteExpedition, name="delete"),
    path('listclass/', ListExpedition.as_view(), name="listclass"),
    path('detailclass/<int:pk>/', DetailExpedition.as_view(), name="detailclass"),
    path('deleteclass/<int:pk>/', DeleteExpedition.as_view(), name="deleteclass"),
    path('createclass/', CreateExpedition.as_view(), name="createclass"),
    path('updateclass/<int:pk>/', UpdateExpedition.as_view(), name="updateclass"),
]
