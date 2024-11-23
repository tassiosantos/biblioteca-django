"""
URL configuration for biblioteca project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from core import views
from core.views import ColecaoListCreate, ColecaoDetail

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('livros/', views.livro_list_create, name='livros-list-create'),
    path('livros/', views.LivroList.as_view(), name='livros-list'),
    path('livros/<int:pk>/', views.LivroDetail.as_view(), name='livro-detail'),
    
    path('categorias/', views.CategoriaList.as_view(), name='categorias-list'),
    path('categorias/<int:pk>/', views.CategoriaDetail.as_view(), name='categoria-detail'),
    
    path('autores/', views.AutorList.as_view(), name='autores-list'),
    path('autores/<int:pk>/', views.AutorDetail.as_view(), name='autor-detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/colecoes/', ColecaoListCreate.as_view(), name='colecao-list-create'),
    path('api/colecoes/<int:pk>/', ColecaoDetail.as_view(), name='colecao-detail'),
]



