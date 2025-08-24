from django.db import models
from accounts.models import UserProfile
from orders.models import OrderItem
from products.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

class Review(models.Model):
    order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE, related_name='order_item_reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_reviews')
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    analysis_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # เรียกใช้ class method โดยไม่ต้องสร้างออบเจ็กต์
    @classmethod
    def get_average_rating(cls, product):
        """ ดึงค่าเฉลี่ยของคะแนนรีวิวของสินค้า """
        return cls.objects.filter(product=product).aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    def __str__(self):
        return f"รีวิว ID: {self.id} โดย {self.user.username}"

class ReviewAnalysis(models.Model):
    POLARITY_CHOICES = [
        ("positive", "คำเชิงบวก"),
        ("negative", "คำเชิงลบ"),
        ("neutral", "เป็นกลาง"),
    ]

    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name="analysis")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="analyses")
    score = models.FloatField()
    polarity = models.CharField(max_length=50, choices=POLARITY_CHOICES, default='neutral')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"การวิเคราะห์รีวิว {self.review.id} - ขั้วอารมณ์: {self.polarity}"

class ReviewSentiment(models.Model):
    SENTIMENT_CHOICES = [
        ('positive', 'คำเชิงบวก'),
        ('negative', 'คำเชิงลบ'),
    ]

    analysis = models.ForeignKey(ReviewAnalysis, on_delete=models.CASCADE, related_name="sentiments")
    sentiment_type = models.CharField(max_length=10, choices=SENTIMENT_CHOICES)
    word = models.CharField(max_length=255)

    def __str__(self):
        return f"วิเคราะห์ ID: {self.analysis.id} | {self.sentiment_type.capitalize()} Word: {self.word}"
