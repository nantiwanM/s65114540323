from django.urls import path
from .views import test, AnalyzeReviewsView, DashboardView, ProductAnalysisListView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('analyze-reviews/', AnalyzeReviewsView.as_view(), name='analyze_reviews'),
    path('product-analysis/', ProductAnalysisListView.as_view(), name='product_analysis'),


    path('test/', test, name='test'),
    # path('product-review-analysis/', ProductReviewAnalysisListView.as_view(), name='product_review_analysis'),

]

