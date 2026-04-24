from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Tour, Destination

class TourCRUDTests(APITestCase):
    def setUp(self):
        # Создаем направление для туров
        self.dest = Destination.objects.create(country="Россия", region="Алтай")
        
        # Данные для создания тура
        self.tour_data = {
            "hotel": "Altay Resort",
            "description": "Классный отель",
            "food_type": "AI",
            "price": "50000.00",
            "stock": 10,
            "destination": self.dest.id
        }

        # Создаем пользователей
        self.admin_user = User.objects.create_superuser(username='admin', password='password123')
        self.common_user = User.objects.create_user(username='user', password='password123')

    def test_create_tour_as_admin(self):
        """Проверка: Админ может создать тур"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('tour-list')
        response = self.client.post(url, self.tour_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tour.objects.count(), 1)

    def test_create_tour_as_user_fail(self):
        """Проверка: Обычный юзер НЕ может создать тур"""
        self.client.force_authenticate(user=self.common_user)
        url = reverse('tour-list')
        response = self.client.post(url, self.tour_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_tours_unauthorized(self):
        """Проверка: Аноним может просматривать список туров"""
        Tour.objects.create(
            hotel="Test", description="...", food_type="NO", 
            price=1000, stock=5, destination=self.dest
        )
        url = reverse('tour-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_tour_as_admin(self):
        """Проверка: Админ может редактировать тур"""
        tour = Tour.objects.create(
            hotel="Old Hotel", description="...", food_type="NO", 
            price=1000, stock=5, destination=self.dest
        )
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('tour-detail', args=[tour.id])
        response = self.client.patch(url, {"hotel": "New Hotel"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tour.refresh_from_db()
        self.assertEqual(tour.hotel, "New Hotel")
