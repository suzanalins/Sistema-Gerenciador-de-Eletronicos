import django_filters
from .models import *


class UsuarioFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(field_name='nome',lookup_expr='icontains')
    tipo = django_filters.CharFilter(field_name='tipo', lookup_expr='iexact')
    class Meta:
        model = Usuario
        fields = ['nome', 'tipo']

class ProdutoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(field_name='nome', lookup_expr='icontains')
    marca = django_filters.CharFilter(field_name='marca', lookup_expr='icontains')
    categoria = django_filters.NumberFilter(field_name='categoria_id')
    estoque_min = django_filters.NumberFilter(field_name='estoque_atual', lookup_expr='gte')
    estoque_max = django_filters.NumberFilter(field_name='estoque_atual', lookup_expr='lte')

    class Meta:
        model = Produto
        fields = ['nome', 'marca', 'categoria']

from .models import Movimentacao

class MovimentacaoFilter(django_filters.FilterSet):
    produto = django_filters.NumberFilter(field_name='produto_id')
    usuario = django_filters.NumberFilter(field_name='usuario_id')
    tipo = django_filters.CharFilter(field_name='tipo_movimentacao', lookup_expr='iexact')
    data_inicio = django_filters.DateFilter(field_name='data_movimentacao', lookup_expr='gte')
    data_fim = django_filters.DateFilter(field_name='data_movimentacao', lookup_expr='lte')

    class Meta:
        model = Movimentacao
        fields = ['produto', 'usuario', 'tipo']


