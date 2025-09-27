from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import ConsultationRequest
from .models import Product, Order, Occasion


def index(request):
    bouquets = Product.objects.filter(is_recommended=True)

    return render(
        request,
        'index.html',
        {
            'bouquets': bouquets,
        }
    )


def catalog(request):
    bouquets = Product.objects.all()

    return render(
        request,
        'catalog.html',
        {
            'bouquets': bouquets,
        }
    )


def bouquet_item(request, bouquet_id):
    bouquet = get_object_or_404(Product, id=bouquet_id)
    composition = bouquet.flower_composition.all()

    if composition:
        flower_strings = []
        for comp in composition:
            text = f'{comp.flower.name} - {comp.quantity} шт.'
            flower_strings.append(text)
        flowers_display = ', '.join(flower_strings)
    else:
        flowers_display = 'Состав не указан'

    return render(
        request,
        'bouquet.html',
        {
            'bouquet': bouquet,
            'flowers_display': flowers_display,
        }
    )


def catalog_collect(request, bouquet_id):
    bouquet = get_object_or_404(Product, id=bouquet_id)
    occasions = bouquet.occasions.all()

    bouquets = (
        Product.objects
        .filter(occasions__in=occasions)
        .distinct()
    )

    return render(
        request,
        'catalog-collect.html',
        {
            'bouquets': bouquets,
        }
    )


def order_step_delivery(request, bouquet_id):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        delivery_address = request.POST.get('delivery_address')
        order_time = request.POST.get('orderTime')

        product = Product.objects.get(pk=bouquet_id)
        order = Order.objects.create(
            customer_name=customer_name,
            customer_phone=customer_phone,
            delivery_address=delivery_address,
            delivery_date=timezone.now().date(),
            comment=order_time or "",
            product=product,
            quantity=1,
        )

        pay_url = reverse("payments:pay", args=[bouquet_id])
        amount = order.total_price
        return redirect(f"{pay_url}?order_id={order.id}&amount={amount}")

    return render(request, 'order.html', {'bouquet_id': bouquet_id})


def quiz_step(request):
    """Обработка квиза"""
    if request.method == 'POST':
        occasion = request.POST.get('occasion')
        price_range = request.POST.get('price_range')

        if occasion and not price_range:
            return render(request, 'quiz-step.html', {
                'step': 2,
                'occasion': occasion,
                'title': 'Какой у вас бюджет?'
            })

        if occasion and price_range:
            bouquets = Product.objects.all()

            if occasion and occasion != 'any':
                bouquets = bouquets.filter(occasions__name__icontains=occasion)

            if price_range:
                if price_range == 'low':
                    bouquets = bouquets.filter(price__lte=1000)
                elif price_range == 'medium':
                    bouquets = bouquets.filter(price__gt=1000, price__lte=5000)
                elif price_range == 'high':
                    bouquets = bouquets.filter(price__gt=5000)

            return render(request, 'catalog.html', {
                'bouquets': bouquets,
                'is_quiz_result': True,
                'selected_occasion': occasion,
                'selected_price': price_range
            })

    return render(request, 'quiz-step.html', {
        'step': 1,
        'title': 'К какому событию нужен букет?'
    })


def consultation(request):
    if request.method == 'POST':
        ConsultationRequest.objects.create(
            customer_name=request.POST.get('fname'),
            customer_phone=request.POST.get('tel'),
        )
        return redirect('core:index')
    return render(request, 'consultation.html')


def result(request):
    return render(request, 'result.html')
