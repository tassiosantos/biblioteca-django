from django.shortcuts import render
from core.filter import AutorFilter, CategoriaFilter, LivroFilter
from rest_framework import generics, permissions

from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Livro, Colecao
from .serializers import LivroSerializer, ColecaoSerializer

from .models import Categoria
from .serializers import CategoriaSerializer

from .models import Autor
from .serializers import AutorSerializer

from .custom_permissions import IsColecionadorOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class LivroList(generics.ListCreateAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    name = "livro-list"
    filterset_class = LivroFilter
    ordering_fields = ['titulo', 'autor', 'categoria', 'publicado_em']
    
    
class LivroDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    name = "livro-detail"
    

class CategoriaList(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    name = "categoria-list"
    filterset_class = CategoriaFilter
    
class CategoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    name = "categoria-detail"
    
    
    
class AutorList(generics.ListCreateAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    name = "autor-list" 
    filterset_class = AutorFilter
    
    
class AutorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    name = "autor-detail"

      
class ColecaoListCreate(generics.ListCreateAPIView):
    queryset = Colecao.objects.all()
    serializer_class = ColecaoSerializer
    name = "colecao-list-create"
    filterset_fields = (
        "nome",
        "descricao",
        "colecionador",
    )
    search_fields = ("^nome",)
    ordering_fields = (
        "nome",
        "descricao",
    )
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def perform_create(self, serializer):
        serializer.save(colecionador=self.request.user)

class ColecaoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Colecao.objects.all()
    serializer_class = ColecaoSerializer
    name = "colecao-detail"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
