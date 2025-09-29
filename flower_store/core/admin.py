from django.contrib import admin
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.urls import reverse

from .models import (ConsultationRequest, Courier, Florist, Flower, Occasion,
                     Order, Product, ProductFlowerComposition, ProductOccasion)

admin.site.unregister(Group)


@admin.register(Occasion)
class OccasionAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count']
    search_fields = ['name']

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = 'Количество букетов'


class ProductOccasionInline(admin.TabularInline):
    model = ProductOccasion
    extra = 1
    verbose_name = 'Повод'
    verbose_name_plural = 'Поводы для букета'


class ProductFlowerCompositionInline(admin.TabularInline):
    model = ProductFlowerComposition
    extra = 1
    verbose_name = 'Цветок в составе'
    verbose_name_plural = 'Состав букета'
    min_num = 1
    validate_min = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'price',
        'primary_occasion',
        'image_preview',
        'order_count',
        'view_customers',
        'is_recommended'
    ]
    list_filter = ['occasions']
    list_editable = ["is_recommended"]
    search_fields = ['name', 'first_description']
    inlines = [ProductOccasionInline, ProductFlowerCompositionInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'is_recommended', 'first_description', 'last_description', 'price', 'image')
        }),
    )

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if not form.instance.productoccasion_set.exists():
            raise ValidationError('Добавьте хотя бы один повод для букета.')

    def primary_occasion(self, obj):
        primary = obj.productoccasion_set.filter(is_primary=True).first()
        return primary.occasion if primary else '-'

    primary_occasion.short_description = 'Основной повод'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return '-'

    image_preview.short_description = 'Фото'

    def order_count(self, obj):
        return obj.orders.count()

    order_count.short_description = 'Заказов'

    def view_customers(self, obj): 
        count = obj.orders.count()
        url = reverse('admin:core_order_changelist') + f'?product__id__exact={obj.id}'
        return format_html('<a href="{}">{} клиентов</a>', url, count)

    view_customers.short_description = 'Клиенты'


@admin.register(Florist)
class FloristAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'consultation_count']
    search_fields = ['name', 'phone', 'email']

    def consultation_count(self, obj):
        return obj.consultation_requests.count()

    consultation_count.short_description = 'Заявки'


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'order_count']
    search_fields = ['name', 'phone']

    def order_count(self, obj):
        return obj.orders.count()

    order_count.short_description = 'Заказы'


@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'customer_name', 'customer_phone', 'product',
        'quantity', 'total_price', 'status', 'created_at', 'delivery_time', 'courier'
    ]
    list_filter = ['status', 'delivery_date', 'created_at', 'product']
    search_fields = ['customer_name', 'customer_phone', 'delivery_address', 'product__name']
    readonly_fields = ['created_at', 'total_price',]
    list_editable = ['status', 'delivery_time']
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('customer_name', 'customer_phone', 'customer_email')
        }),
        ('Доставка', {
            'fields': ('delivery_address', 'delivery_date', 'delivery_time', 'courier')
        }),
        ('Заказ', {
            'fields': ('product', 'quantity', 'total_price', 'status')
        }),
        ('Дополнительно', {
            'fields': ('comment', 'created_at')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product', 'courier')


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'customer_name', 'customer_phone', 'status',
        'florist', 'created_at', 'is_processed'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'customer_phone']
    readonly_fields = ['created_at', 'processed_at']
    list_editable = ['status', 'florist']
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('customer_name', 'customer_phone', 'comment')
        }),
        ('Обработка', {
            'fields': ('status', 'florist', 'processed_at')
        }),
        ('Системная информация', {
            'fields': ('created_at',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('florist')


admin.site.site_header = 'Администрирование цветочного магазина'
admin.site.site_title = 'Цветочный магазин'
admin.site.index_title = 'Панель управления'
