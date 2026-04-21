from django.contrib import admin
from .models import Destination, Tour, Customer, Agent, Booking
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('country', 'region')
    search_fields = ('country', 'region')

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'destination', 'food_type', 'price')
    list_filter = ('food_type', 'destination')
    search_fields = ('hotel',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_full_name', 'phone', 'passport')
    search_fields = ('user__username', 'phone', 'passport') 
    @admin.display(description='Логин')
    def get_username(self, obj):
        return obj.user.username

    @admin.display(description='ФИО')
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"



# Настройка вложенного интерфейса
class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    verbose_name_plural = 'Дополнительная информация (Клиент)'

# Переопределяем стандартный UserAdmin
class UserAdmin(BaseUserAdmin):
    inlines = (CustomerInline,)

# Перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'internal_phone')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'tour', 'start_date', 'status', 'total_price', 'agent')
    list_filter = ('status', 'start_date', 'agent')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)

