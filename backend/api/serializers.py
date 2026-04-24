from rest_framework import serializers
from .models import Tour, Booking, Destination, Customer
from django.db import transaction

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        # total_price и price_at_booking вычисляем, customer берем из запроса
        read_only_fields = ('total_price', 'price_at_booking', 'customer', 'status', 'agent')

    def validate(self, attrs):
        tour = attrs['tour']
        people_count = attrs['people_count']

        # 1. Проверяем наличие мест на складе (stock)
        if tour.stock < people_count:
            raise serializers.ValidationError(
                f"Недостаточно мест. Доступно: {tour.stock}, запрошено: {people_count}"
            )
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        # Получаем текущего пользователя (клиента)
        user = self.context['request'].user
        customer = Customer.objects.get(user=user)
        
        tour = validated_data['tour']
        people_count = validated_data['people_count']

        # 2. Фиксируем цену на момент заказа и считаем общую сумму
        validated_data['customer'] = customer
        validated_data['price_at_booking'] = tour.price
        validated_data['total_price'] = tour.price * people_count

        # 3. Уменьшаем stock у товара
        tour.stock -= people_count
        tour.save()

        return super().create(validated_data)
