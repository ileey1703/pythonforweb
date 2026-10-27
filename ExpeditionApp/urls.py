from .views import *
from django.urls import path


urlpatterns =[
    path('home/', home, name='home'),
    path('w/<str:name>' , welcome, name="welcomeFunction"),
    path('list/', listExpedition , name="list"),
    path('detail/<int:pk>/', detailExpedition, name="detail"),
    path('delete/<int:pk>/', deleteExpedition, name="delete"),
]
