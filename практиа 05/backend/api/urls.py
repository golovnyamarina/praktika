from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import TourViewSet, BookingViewSet

# Роутер автоматически создает пути для CRUD (GET, POST, PUT, DELETE)
router = DefaultRouter()
router.register(r'tours', TourViewSet, basename='tour')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    # Пути для получения и обновления токена (логин)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Подключаем все маршруты из роутера
    path('', include(router.urls)),
]
