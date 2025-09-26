from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('result/', views.result, name='result'),
    path('bouquet/<int:bouquet_id>/', views.bouquet_item, name='bouquet_item'),
    path('consultation/', views.consultation, name='consultation'),
    path('catalog-collect/<int:bouquet_id>/', views.catalog_collect, name='catalog_collect'),
    path('order_step_delivery/<int:bouquet_id>/', views.order_step_delivery, name='order_step_delivery'),
]
