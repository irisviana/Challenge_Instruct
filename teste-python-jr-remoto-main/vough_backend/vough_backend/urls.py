"""vough_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Vough API",
      default_version='v1',
      description=" A Vough API:\n"+
      "1 - Buscar organização pelo login através da API do Github\n"+
      "2 - Armazenar os dados atualizados da organização no banco\n"+
      "3 - Retornar corretamente os dados da organização\n"+
      "4 - Retornar os dados de organizações ordenados pelo score na listagem da API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="vianasantana21@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("api.routes"), name="api"),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
