from rest_framework import viewsets, permissions
from .models import Tour, Booking
from .serializers import TourSerializer, BookingSerializer

class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()] # Просмотр доступен всем
        return [permissions.IsAdminUser()] # CRUD только для админов

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        # Админ видит всё, обычный юзер — только свои заявки
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(customer__user=self.request.user)

    def perform_create(self, serializer):
        # АВТОМАТИКА (Задание №4)
        tour = serializer.validated_data['tour']
        people = serializer.validated_data['people_count']
        
        # 1. Расчет суммы
        total = tour.price * people
        
        # 2. Сохраняем с привязкой к текущему клиенту
        # (Предполагаем, что у юзера есть связанный Customer)
        serializer.save(
            customer=self.request.user.customer, 
            total_price=total
        )

