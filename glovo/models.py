from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser должен иметь is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150, blank=True)
    phone = PhoneNumberField(blank=True)
    user_image = models.ImageField(upload_to='user_image', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Restaurant(models.Model):
    STATUS_CHOICES = (
        ('active', 'Активен'),
        ('inactive', 'Неактивен'),
    )

    name = models.CharField(max_length=64, unique=True)
    restaurant_photo = models.ImageField(upload_to='restaurant_photo/')
    description = models.TextField()
    address = models.CharField(max_length=120)
    hours = models.CharField(max_length=64)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MenuCategory(models.Model):
    menu_photo = models.ImageField(upload_to='menu_photo/')
    menu_name = models.CharField(max_length=64)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_categories')

    def __str__(self):
        return f'{self.menu_name}, {self.restaurant}'


class MenuItem(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    price = models.PositiveIntegerField()
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='menu_items')
    photo = models.ImageField(upload_to='menu_item_image/')

    def __str__(self):
        return f'{self.name}, {self.category}'


class Courier(models.Model):
    STATUS_CHOICES = (
        ('free', 'Свободен'),
        ('busy', 'Занят'),
        ('offline', 'Офлайн'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='courier_profile')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='offline')
    current_location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Курьер: {self.user.name}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('created', 'Создан'),
        ('preparing', 'Готовится'),
        ('on_the_way', 'В пути'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries')
    total_price = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk} - {self.user.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()  # Цена за единицу

    def __str__(self):
        return f"{self.menu_item.name} × {self.quantity}"


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    house = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.city}, {self.street} {self.house}"


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = self.restaurant.name if self.restaurant else f"Courier {self.courier.user.name}"
        return f"{self.user.email} → {target}"


class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидается'),
        ('paid', 'Оплачено'),
        ('failed', 'Ошибка'),
        ('cancelled', 'Отменено'),
    )

    METHOD_CHOICES = (
        ('card', 'Карта'),
        ('cash', 'Наличные'),
        ('wallet', 'Кошелек'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='card')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=128, null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.order.id} - {self.status}"
