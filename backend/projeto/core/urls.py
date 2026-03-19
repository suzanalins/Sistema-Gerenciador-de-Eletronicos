from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsuarioViewSet,
    CategoriaViewSet,
    ProdutoViewSet,
    MovimentacaoViewSet,
    login
)

router = DefaultRouter()
router.register('usuarios', UsuarioViewSet)
router.register('categorias', CategoriaViewSet)
router.register('produtos', ProdutoViewSet)
router.register('movimentacoes', MovimentacaoViewSet)

urlpatterns = [
    path('login/', login),
    path('', include(router.urls)),
]