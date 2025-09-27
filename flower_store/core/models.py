from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Occasion(models.Model):
    name = models.CharField(
        max_length=25,
        verbose_name='Повод'
    )

    class Meta:
        verbose_name = 'Повод'
        verbose_name_plural = 'Поводы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Florist(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Имя флориста'
    )
    phone = PhoneNumberField(
        verbose_name='Телефон',
        db_index=True,
        region='RU'
    )
    email = models.EmailField(
        verbose_name='Email'
    )

    class Meta:
        verbose_name = 'Флорист'
        verbose_name_plural = 'Флористы'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"


class Courier(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name='Имя курьера'
    )
    phone = PhoneNumberField(
        verbose_name='Телефон',
        region='RU'
    )

    class Meta:
        verbose_name = 'Курьер'
        verbose_name_plural = 'Курьеры'

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название букета',
        unique=True
    )
    is_recommended = models.BooleanField(
        default=False,
        verbose_name="Рекомендуемый букет"
    )
    first_description = models.TextField(
        verbose_name='Описание букета'
    )
    last_description = models.TextField(
        verbose_name='Общее описание букета',
        blank=True,
        null=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Цена'
    )
    occasions = models.ManyToManyField(
        Occasion,
        through='ProductOccasion',
        verbose_name='Поводы',
        related_name='products'
    )
    image = models.ImageField(
        verbose_name='Фотография букета'
    )

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'

    def __str__(self):
        return f"{self.name} - {self.price} руб."

    def get_primary_occasion(self):
        """Возвращает основной повод"""
        primary = self.productoccasion_set.filter(is_primary=True).first()
        return primary.occasion if primary else None

    def clean(self):
        super().clean()
        if self.is_recommended:
            recommended = Product.objects.filter(is_recommended=True)
            if self.pk:
                recommended = recommended.exclude(pk=self.pk)
            if recommended.count() >= 3:
                raise ValidationError({
                    "is_recommended": "Можно выбрать не более 3 рекомендуемых букетов."
                })


class ProductOccasion(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Букет'
    )
    occasion = models.ForeignKey(
        Occasion,
        on_delete=models.CASCADE,
        verbose_name='Повод'
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name='Основной повод'
    )

    class Meta:
        verbose_name = 'Связь букет-повод'
        verbose_name_plural = 'Связи букет-повод'
        unique_together = ['product', 'occasion']


class Flower(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название цветка',
        unique=True
    )

    class Meta:
        verbose_name = 'Цветок'
        verbose_name_plural = 'Цветы'

    def __str__(self):
        return self.name


class ProductFlowerComposition(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='flower_composition'
    )
    flower = models.ForeignKey(
        Flower,
        on_delete=models.CASCADE,
        verbose_name='Цветок'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )

    def __str__(self):
        return f"{self.flower.name} - {self.quantity} шт."


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        NEW = 'new', 'Новый'
        PAID = 'paid', 'Оплачен'
        ASSIGNED = 'assigned', 'Передан курьеру'
        DELIVERED = 'delivered', 'Доставлен'
        CANCELLED = 'cancelled', 'Отменен'

    customer_name = models.CharField(
        max_length=50,
        verbose_name='Имя клиента'
    )
    customer_phone = PhoneNumberField(
        verbose_name='Телефон клиента',
        region='RU'
    )
    customer_email = models.EmailField(
        blank=True,
        verbose_name='Email клиента'
    )
    delivery_address = models.TextField(
        verbose_name='Адрес доставки'
    )
    delivery_date = models.DateField(
        verbose_name='Дата доставки'
    )
    CHOICE = (
        ('any', 'Как можно скорее')
        ('10-12', '10:00 - 12:00'),
        ('12-14', '12:00 - 14:00'),
        ('14-16', '14:00 - 16:00'),
        ('16-18', '16:00 - 18:00'),
        ('18-20', '18:00 - 20:00'),
    )
    delivery_time = models.CharField(
        verbose_name='Время доставки',
        max_length=20,
        choices=CHOICE,
        default='any')
    courier = models.ForeignKey(
        Courier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Курьер',
        related_name='orders'
    )
    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий к заказу'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='Букет',
        related_name='orders'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Общая стоимость',
        editable=False  # Делаем поле нередактируемым в админке
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.NEW,
        verbose_name='Статус заказа'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания заказа'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} - {self.customer_name} ({self.status})"

    def calculate_total_price(self):
        if self.product and self.quantity:
            return self.product.price * self.quantity
        return 0

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()

        if self.status == self.OrderStatus.DELIVERED and not self.delivered_at:
            self.delivered_at = timezone.now()
        elif self.status != self.OrderStatus.DELIVERED:
            self.delivered_at = None

        super().save(*args, **kwargs)

    @property
    def formatted_total_price(self):
        return f"{self.total_price} руб."

    @property
    def product_price(self):
        return self.product.price if self.product else 0


class ConsultationRequest(models.Model):
    class RequestStatus(models.TextChoices):
        NEW = 'new', 'Новая'
        IN_PROGRESS = 'in_progress', 'В работе'
        COMPLETED = 'completed', 'Завершена'

    customer_name = models.CharField(
        max_length=100,
        verbose_name='Имя клиента'
    )
    customer_phone = PhoneNumberField(
        max_length=20,
        verbose_name='Телефон клиента',
        region='RU'
    )
    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий клиента'
    )

    status = models.CharField(
        max_length=20,
        choices=RequestStatus.choices,
        default=RequestStatus.NEW,
        verbose_name='Статус заявки'
    )
    florist = models.ForeignKey(
        Florist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Назначенный флорист',
        related_name='consultation_requests'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания заявки'
    )
    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата обработки заявки'
    )

    @property
    def is_processed(self):
        return self.status != self.RequestStatus.NEW and self.florist is not None

    def save(self, *args, **kwargs):
        if self.florist and not self.processed_at:
            self.processed_at = timezone.now()
        elif not self.florist:
            self.processed_at = None

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Заявка на консультацию'
        verbose_name_plural = 'Заявки на консультацию'
        ordering = ['-created_at']

    def __str__(self):
        return f'Консультация #{self.id} - {self.customer_name} ({self.status})'
