from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from .filters import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import*
from .serializers import *


###VIEWS


#usuário
class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Usuario.objects.filter(user=self.request.user)
    
    


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"Usuário criado com sucesso."}, status=status.HTTP_201_CREATED)
    


class MeView(RetrieveAPIView):
    serializer_class = UsuarioMeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        perfil, created = Usuario.objects.get_or_create(
            user=self.request.user,
            defaults={
                'nome': self.request.user.username,
            }
        )
        return perfil



#categoria
class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]


#produto
class ProdutoViewSet(ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categoria']
    filterset_class = ProdutoFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.query_params.get('nome')

        if nome:
            queryset = queryset.filter(nome__icontains=nome)

        return queryset


#MOVIMENTAÇÃO
class MovimentacaoViewSet(ModelViewSet):
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['produto', 'tipo_movimentacao']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        produto = serializer.instance.produto
        response_data = serializer.data

        #ALERTA DE ESTOQUE
        if produto.estoque_atual < produto.estoque_minimo:
            response_data['alerta'] = 'Estoque abaixo do mínimo!'

        return Response(response_data, status=status.HTTP_201_CREATED)