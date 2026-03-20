from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('usuarios', UsuarioViewSet)
router.register('categorias', CategoriaViewSet)
router.register('produtos', ProdutoViewSet)
router.register('movimentacoes', MovimentacaoViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('me/', MeView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('', include(router.urls)),
]