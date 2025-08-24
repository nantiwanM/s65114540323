from django.contrib import admin
from dashboard.models import Review, ReviewAnalysis, ReviewSentiment

admin.site.register(Review)
admin.site.register(ReviewAnalysis)
admin.site.register(ReviewSentiment)
