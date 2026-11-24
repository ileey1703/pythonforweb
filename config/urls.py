"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from config.admin import admin_site
from django.contrib.auth.views import LoginView, LogoutView
from EntrepriseApp.views import registerUser  # Import the registerUser view    
urlpatterns = [
    path('admin/', admin_site.urls),
    path('expedition/', include('ExpeditionApp.urls')),
    path('entreprises/', include('EntrepriseApp.urls')),
    path('offres/', include('OffreApp.urls')),
    path('vehicules/', include('VehiculeApp.urls')),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', registerUser, name='register'),

]
