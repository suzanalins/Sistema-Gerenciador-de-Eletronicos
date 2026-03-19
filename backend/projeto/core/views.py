from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, APIView
from .filters import ProdutoFilter, UsuarioFilter, MovimentacaoFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Produto
from .serializers import ProdutoSerializer
from .models import Usuario, Categoria, Produto, Movimentacao
from .serializers import (
    UsuarioSerializer,
    CategoriaSerializer,
    ProdutoSerializer,
    MovimentacaoSerializer
)




#usuário
class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]



class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"Usuário criado com sucesso."}, status=status.HTTP_201_CREATED)



# LOGIN
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    senha = request.data.get('senha')

    if not email or not senha:
        return Response(
            {'erro': 'Email e senha são obrigatórios'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        usuario = Usuario.objects.get(email=email, senha=senha)

        return Response({
            'mensagem': 'Login realizado com sucesso',
            'usuario': {
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email,
                'tipo_usuario': usuario.tipo_usuario
            }
        }, status=status.HTTP_200_OK)

    except Usuario.DoesNotExist:
        return Response(
            {'erro': 'Email ou senha inválidos'},
            status=status.HTTP_400_BAD_REQUEST
        )


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

        produto = serializer.validated_data['produto']
        response_data = serializer.data

        #ALERTA DE ESTOQUE
        if produto.estoque_atual < produto.estoque_minimo:
            response_data['alerta'] = 'Estoque abaixo do mínimo!'

        return Response(response_data, status=status.HTTP_201_CREATED)