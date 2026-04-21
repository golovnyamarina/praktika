from rest_framework import serializers
from .models import Tour, Booking, Destination

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('total_price', 'customer', 'status') # Эти поля считаем автоматом
