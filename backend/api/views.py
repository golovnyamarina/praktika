from rest_framework import viewsets, permissions
from .models import Tour, Booking, Destination
from .serializers import TourSerializer, BookingSerializer

class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

    def get_permissions(self):
        # Неавторизованный — только просмотр (п. 3)
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        # Администратор — CRUD (п. 3)
        return [permissions.IsAdminUser()]

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer

    def get_permissions(self):
        # Создавать и смотреть свои может только авторизованный (п. 3)
        if self.action in ['create', 'list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        # Удалять или менять статус (CRUD) — только админ
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        # Разграничение видимости (п. 3)
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        # Обычный пользователь видит только свои заявки
        return Booking.objects.filter(customer__user=user)

    def perform_create(self, serializer):
        # ВСЯ ЛОГИКА ИЗ ПУНКТА 4 (Проверка, списание, расчет)
        tour = serializer.validated_data['tour']
        people = serializer.validated_data['people_count']
        
        # Проверка наличия (хотя лучше дублировать в сериализаторе для красоты)
        if tour.stock < people:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("На складе недостаточно мест!")

        # Уменьшаем stock
        tour.stock -= people
        tour.save()

        # Расчет и фиксация цены (п. 4)
        total = tour.price * people
        serializer.save(
            customer=self.request.user.customer,
            price_at_booking=tour.price, # Фиксируем цену из тура
            total_price=total
        )
