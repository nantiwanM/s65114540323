from django.urls import path
from articles.views import ArticleListView,ArticleCreateView, ArticleUpdateView, ArticleDeleteView, ShopArticleListView, ArticleDetailView

urlpatterns = [
    path('admin/article/list/', ArticleListView.as_view(), name='article_list' ),
    path('admin/article/create/', ArticleCreateView.as_view(), name='article_create' ),
    path('admin/article/edit/<int:pk>/', ArticleUpdateView.as_view(), name='article_edit'),
    path('admin/article/delete/<int:pk>/', ArticleDeleteView.as_view(), name='article_delete'),


    path('articles/', ShopArticleListView.as_view(), name='articles'),
    path('article/detail/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
]