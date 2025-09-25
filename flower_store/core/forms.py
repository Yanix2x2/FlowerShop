from django import forms

from .models import ConsultationRequest, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer_name',
            'customer_phone',
            'customer_email',
            'delivery_address',
            'delivery_date',
            'comment',
            'product',
            'quantity',
        ]


class ConsultationRequestForm(forms.ModelForm):
    class Meta:
        model = ConsultationRequest
        fields = ['customer_name', 'customer_phone', 'comment']
