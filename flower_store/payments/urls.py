from django.urls import path
from . import views


app_name = "payments"

urlpatterns = [
    path("pay/<int:bouquet_id>/", views.pay, name="pay"),
    path("success/", views.success, name="success"),
    path("fail/", views.fail, name="fail"),
]
