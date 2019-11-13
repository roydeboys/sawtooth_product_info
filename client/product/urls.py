from django.urls import path, include
from .views import InsertProduct, CheckProduct

urlpatterns = [
    path('insert/', InsertProduct.as_view()),
    path('check/<product_id>/', CheckProduct.as_view()),
]
