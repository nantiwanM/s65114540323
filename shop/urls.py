from django.urls import path
from shop.views import ShopListView, ProductDetailView, ProductOptionView, ReviewListView, SearchResultsView

urlpatterns = [
    path('', ShopListView.as_view(), name='shop'),
    path("search/", SearchResultsView.as_view(), name="search_results"),

    path('product/<int:pk>/', ProductDetailView.as_view(), name="product_detail"),
    path("product/<int:pk>/options/", ProductOptionView.as_view(), name="product-options"),
    path("product/<int:product_id>/reviews/", ReviewListView.as_view(), name="load_reviews"),

]