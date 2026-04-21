from django.db import models
from django.contrib.auth.models import User

#направление
class Destination(models.Model):
    country = models.CharField(max_length=100, verbose_name="Страна")
    region = models.CharField(max_length=150, verbose_name="Регион")

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'

    def __str__(self):
        return f'{self.country} - {self.region}'

#тур
class Tour(models.Model):
    FOOD_TYPE = [
        ('AI','Всё включено'),
        ('OB','Только завтраки'),
        ('BD','Завтрак и ужин'),
        ('NO','Нет питания'),
    ]
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, verbose_name="Направление")
    hotel = models.CharField(max_length=200, verbose_name="Отель")
    description = models.TextField(verbose_name="Описание")
    food_type = models.CharField(max_length=2, choices=FOOD_TYPE, verbose_name="Тип питания")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость за человека")

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'

    def __str__(self):
        return f'{self.hotel} - {self.destination}, {self.price}'  
      
#клиент
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    passport = models.CharField(max_length=10, verbose_name="Серия и номер паспорта")

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.phone}'

#агент
class Agent(models.Model):
    full_name = models.CharField(max_length=250, verbose_name="ФИО")
    position = models.CharField(max_length=100, verbose_name="Должность")
    internal_phone = models.CharField(max_length=10, blank=True, verbose_name="Внутренний номер")

    class Meta:
        verbose_name = 'Агент'
        verbose_name_plural = 'Агенты'

    def __str__(self):
        return f'{self.full_name}'
    
#бронь
class Booking(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Новая заявка'),
        ('PRC', 'В обработке'),
        ('PAY', 'Оплачено'),
        ('CAN', 'Отменено'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Клиент")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name="Тур")
    start_date = models.DateField(verbose_name='Дата начала поездки')
    end_date = models.DateField(verbose_name='Дата окончания поездки')

    people_count = models.PositiveIntegerField(default=1, verbose_name='Количество человек')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Итоговая стоимость')

    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='NEW', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания брони')
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    def __str__(self):
        return f'{self.customer} - {self.agent}, {self.tour}'