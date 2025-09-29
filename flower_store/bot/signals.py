from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from core.models import Order, ConsultationRequest
from .notifications import send_telegram_message


@receiver(post_save, sender=Order)
def order_paid_handler(sender, instance: Order, created, **kwargs):
    if instance.status == Order.OrderStatus.PAID:
        courier_text = (
            f"🚚 Новый заказ для доставки!\n\n"
            f"Курьер: {instance.courier.name}\n\n"
            f"Адрес: {instance.delivery_address}\n"
            f"Дата: {instance.delivery_date}, {instance.get_delivery_time_display()}\n"
            f"Получатель: {instance.customer_name}, {instance.customer_phone}\n"
            f"Товар: {instance.product} × {instance.quantity}\n"
            f"Сумма: {instance.total_price} ₽"
        )
        send_telegram_message(settings.TELEGRAM_GROUP_CHAT_ID, courier_text)

        instance.status = Order.OrderStatus.ASSIGNED


@receiver(post_save, sender=ConsultationRequest)
def consultation_request_created(sender, instance: ConsultationRequest, created, **kwargs):
    if created:
        text = (
            f"💬 Новая заявка на консультацию!\n\n"
            f"Имя: {instance.customer_name}\n"
            f"Телефон: {instance.customer_phone}\n"
            f"Комментарий: \n{instance.comment or '—'}"
        )
        send_telegram_message(settings.TELEGRAM_GROUP_CHAT_ID, text)

        instance.status = ConsultationRequest.RequestStatus.IN_PROGRESS
        instance.save(update_fields=["status"])
