from django.urls import path
from .views import AddToCartView, CartDetailView, RemoveCartItemView, UpdateCartView

urlpatterns = [
    path('add/<int:product_id>', AddToCartView.as_view(), name='add_cart'),
    path("", CartDetailView.as_view(), name="cart_detail"),
    path('update/<int:pk>/', UpdateCartView.as_view(), name='update_cart'),
    path("remove/<int:pk>/", RemoveCartItemView.as_view(), name="remove_cart_item"),
]