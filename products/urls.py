from django.urls import path
from .views import ProductListView,ProductCreateView, ProductEditView, ProductDeleteView, DeleteImageView

urlpatterns = [
 path('product/list', ProductListView.as_view(), name="product_list"),
 path('product/create/', ProductCreateView.as_view(), name="product_create"),
 path('product/edit/<int:pk>/', ProductEditView.as_view(), name='product_edit'),
 path('product/delete-image/<int:image_id>/', DeleteImageView.as_view(),  name='delete_image'),
 path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),

]