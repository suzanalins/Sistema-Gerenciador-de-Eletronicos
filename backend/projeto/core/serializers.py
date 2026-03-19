from rest_framework import serializers
from .models import Usuario, Categoria, Produto, Movimentacao


#tabela de usuários
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'senha', 'tipo_usuario']
        extra_kwargs = {
            'senha': {'write_only': True}
        }

    def create(self, validated_data):
        return Usuario.objects.create(**validated_data)

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