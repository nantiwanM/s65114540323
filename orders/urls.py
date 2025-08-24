from django.urls import path
from .views import OrderListView, OrderDetailView, CartCheckoutView, BuyNowView, PaymentView, MyOrdersView, \
    CancelOrderView, ReviewView

urlpatterns = [
    path('admin/order/list', OrderListView.as_view(), name='order_list'),
    path('admin/order/detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('buy-now/', BuyNowView.as_view(), name='buy_now'),
    path("checkout/", CartCheckoutView.as_view(), name="checkout"),
    path('payment/<int:order_id>/', PaymentView.as_view(), name='payment'),
    path("my-orders/", MyOrdersView.as_view(), name="my_orders"),
    path('cancel_order/<int:order_id>/', CancelOrderView.as_view(), name='cancel_order'),
    path('review/<int:item_id>/', ReviewView.as_view(), name='review'),

]