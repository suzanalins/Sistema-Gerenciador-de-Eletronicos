from rest_framework import serializers
from .models import Usuario, Categoria, Produto, Movimentacao
from django.contrib.auth.models import User


##SERIALIZERS


#tabela de usuários
class UsuarioSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source ='user.username', read_only = True)
    email = serializers.CharField(source ='user.email', read_only = True)

    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'username', 'email']



class RegisterSerializer(serializers.Serializer):
    # Tabela auth_user
    username =  serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    # Tabela api_usuario 
    nome = serializers.CharField(required=False, allow_blank=True, default='')
   


    def create(self, validated_data):
        # Criando na Tabela api_usuario 
        nome = validated_data.get('nome', '')
        email = validated_data['email']
        senha= validated_data.get('senha', '')


        # Criando na Tabela auth_user 
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
  
        user.is_active = True
     
        Usuario.objects.create(
            user = user,
            nome = nome if nome else user.username
        )

        return user



#usuario me serializer
class UsuarioMeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'username', 'is_active']










#tabela de categorias
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


#tabela de produtos
class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)

    class Meta:
        model = Produto
        fields = [
            'id',
            'nome',
            'descricao',
            'marca',
            'tensao',
            'armazenamento',
            'resolucao_tela',
            'conectividade',
            'estoque_atual',
            'estoque_minimo',
            'categoria',
            'categoria_nome'
        ]

    def validate(self, data):
        if data['estoque_minimo'] < 0:
            raise serializers.ValidationError("Estoque mínimo não pode ser negativo")

        if data['estoque_atual'] < 0:
            raise serializers.ValidationError("Estoque atual não pode ser negativo")

        return data


#tabela de movimentações
class MovimentacaoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    usuario_nome = serializers.CharField(source='usuario.nome', read_only=True)

    class Meta:
        model = Movimentacao
        fields = [
            'id',
            'produto',
            'produto_nome',
            'usuario',
            'usuario_nome',
            'tipo_movimentacao',
            'quantidade',
            'data_movimentacao'
        ]

    def validate(self, data):
        produto = data['produto']
        tipo = data['tipo_movimentacao']
        quantidade = data['quantidade']

        if quantidade <= 0:
            raise serializers.ValidationError("Quantidade deve ser maior que zero")

        if tipo == 'saida' and produto.estoque_atual < quantidade:
            raise serializers.ValidationError("Estoque insuficiente para saída")

        return data

    def create(self, validated_data):
        produto = validated_data['produto']
        tipo = validated_data['tipo_movimentacao']
        quantidade = validated_data['quantidade']

        # Atualiza estoque automaticamente
        if tipo == 'entrada':
            produto.estoque_atual += quantidade
        else:
            produto.estoque_atual -= quantidade

        produto.save()

        return Movimentacao.objects.create(**validated_data)