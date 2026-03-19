from django.db import models


#criando a tabela de usuários
class Usuario(models.Model):
    TIPO_USUARIO = [
        ('administrador', 'Administrador'),
        ('operador', 'Operador'),
    ]

    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO)

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

    estoque_atual = models.IntegerField()
    estoque_minimo = models.IntegerField()

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
    quantidade = models.IntegerField()
    data_movimentacao = models.DateField()

    def __str__(self):
        return f"{self.produto.nome} - {self.tipo_movimentacao}"
