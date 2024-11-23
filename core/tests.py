from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Livro, Colecao, Autor, Categoria
from rest_framework.authtoken.models import Token


class ColecaoTests(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

        self.user2 = User.objects.create_user(username='testuser2', password='testpassword2')
        self.token2 = Token.objects.create(user=self.user2)


        self.autor = Autor.objects.create(nome='Autor Teste')
        self.categoria = Categoria.objects.create(nome='Categoria Teste')
        self.livro = Livro.objects.create(
            titulo='Livro Teste',
            autor=self.autor,
            categoria=self.categoria,
            publicado_em='2023-01-01'
        )


        self.colecao_data = {
            'nome': 'Colecao Teste',
            'descricao': 'Descricao Teste',
            'livros': [self.livro.id]
        }

    def authenticate(self, user):
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_colecao_authenticated(self):
        self.authenticate(self.user)
        response = self.client.post('/api/colecoes/', self.colecao_data, format='json')
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Colecao.objects.count(), 1)
        self.assertEqual(Colecao.objects.get().colecionador, self.user)

    def test_create_colecao_unauthenticated(self):
        response = self.client.post('/api/colecoes/', self.colecao_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_colecao_authenticated(self):
        self.authenticate(self.user)
        colecao = Colecao.objects.create(
            nome='Colecao Teste',
            descricao='Descricao Teste',
            colecionador=self.user
        )
        response = self.client.put(
            f'/api/colecoes/{colecao.id}/',
            {'nome': 'Novo Nome', 'descricao': 'Nova Descricao', 'livros': [self.livro.id]},
            format='json'
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        colecao.refresh_from_db()
        
        self.assertEqual(colecao.nome, 'Novo Nome')

    def test_update_colecao_unauthenticated(self):
        colecao = Colecao.objects.create(
            nome='Colecao Teste',
            descricao='Descricao Teste',
            colecionador=self.user
        )
        response = self.client.put(
            f'/api/colecoes/{colecao.id}/',
            {'nome': 'Novo Nome', 'descricao': 'Nova Descricao', 'livros': [self.livro.id]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_colecao_authenticated(self):
        self.authenticate(self.user)
        colecao = Colecao.objects.create(
            nome='Colecao Teste',
            descricao='Descricao Teste',
            colecionador=self.user
        )
        response = self.client.delete(f'/api/colecoes/{colecao.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Colecao.objects.count(), 0)

    def test_list_colecoes_authenticated(self):
        self.authenticate(self.user)
        Colecao.objects.create(
            nome='Colecao Teste',
            descricao='Descricao Teste',
            colecionador=self.user
        )
        response = self.client.get('/api/colecoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_colecoes_unauthenticated(self):
        Colecao.objects.create(
            nome='Colecao Teste',
            descricao='Descricao Teste',
            colecionador=self.user
        )
        response = self.client.get('/api/colecoes/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
