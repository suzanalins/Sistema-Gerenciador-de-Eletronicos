from django.db import models
from django.contrib.auth.models import User

#criando a tabela de usuários
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # email = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


#criando a tabela de categorias
class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


#criando a tabela de produtos
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    tensao = models.CharField(max_length=10, blank=True, null=True)
    armazenamento = models.CharField(max_length=50, blank=True, null=True)
    resolucao_tela = models.CharField(max_length=50, blank=True, null=True)
    conectividade = models.CharField(max_length=50, blank=True, null=True)

    estoque_atual = models.PositiveIntegerField()#deixa pedindo um valor positivo
    estoque_minimo = models.PositiveIntegerField()

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


#criando a tabela de movimentações
class Movimentacao(models.Model):
    TIPO_MOVIMENTACAO = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    tipo_movimentacao = models.CharField(max_length=10, choices=TIPO_MOVIMENTACAO)
    quantidade = models.PositiveIntegerField()
    data_movimentacao = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.produto.nome} - {self.tipo_movimentacao}"
