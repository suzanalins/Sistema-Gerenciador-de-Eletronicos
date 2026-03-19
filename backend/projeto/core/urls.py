from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)#aqui importa o token e dps cria ele no insomnia e no json coloca requuisição de username e password e la coloca seu super user
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
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('register/', RegisterView.as_view(), name='register'),
]