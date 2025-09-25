from django.shortcuts import get_object_or_404, redirect, render

from .forms import ConsultationRequest
from .models import Product


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

    return render(request, 'order.html')


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

