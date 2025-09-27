from django.shortcuts import render, redirect
from django.http import HttpResponse
from core.models import Order, Courier


def pay(request, bouquet_id: int):
    amount = request.GET.get("amount", "10.00")
    order_id = request.GET.get("order_id")
    ctx = {
        "bouquet_id": bouquet_id,
        "amount": amount,
        "order_id": order_id,
        "PUBLIC_ID": "test_api_00000000000000000000001",
    }
    return render(request, "order-step.html", ctx)


def success(request):
    order_id = request.GET.get("order_id")

    order = Order.objects.get(pk=order_id)
    order.status = Order.OrderStatus.PAID

    if not order.courier:
        from django.db.models import Count
        free_courier = Courier.objects.annotate(
            order_count=Count('orders')
        ).order_by('order_count').first()
        
        if free_courier:
            order.courier = free_courier

    order.save()

    return redirect('core:index')


def fail(request):
    return HttpResponse("Оплата отклонена")
