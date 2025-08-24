from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View

from django.shortcuts import get_object_or_404

from dashboard.models import Review, ReviewAnalysis
from products.models import Product
from django.db.models import F, Min, Max, Count, Q, Sum
from django.shortcuts import render

class ShopListView(ListView):
    model = Product
    template_name = 'shop/shop.html'
    context_object_name = 'products'

    # ใช้ options (related_name) เพื่อเข้าถึงฟิลด์ price ในโมเดล ProductOption
    def get_queryset(self):
        return Product.objects.annotate(min_price=Min('options__price')).order_by('-created_at')[:20]

class SearchResultsView(ListView):
    model = Product
    template_name = "shop/search_results.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('search', '').strip()
        category = self.request.GET.get('category', '')
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")

        products = Product.objects.all().annotate(min_price=Min('options__price'))

        if query:
            products = products.filter(name__icontains=query)

        if category:
            products = products.filter(category=category)

        if min_price:
            products = products.filter(min_price__gte=min_price)

        if max_price:
            products = products.filter(min_price__lte=max_price)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query_params = self.request.GET.copy()  # คัดลอก query parameters
        query_params.pop('page', None)  # ลบพารามิเตอร์ 'page'

        context["categories"] = Product.CATEGORY_CHOICES
        context['query_params'] = query_params.urlencode()  # แปลงเป็น query string ที่ใช้ใน URL

        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ดึงสินค้าปัจจุบัน
        product = self.get_object()

        # ดึงรูปภาพที่เกี่ยวข้องกับสินค้า
        images = product.images.all()

        # วิเคราะห์รีวิวสินค้า
        review_data = ReviewAnalysis.objects.filter(product=product).values_list("polarity", flat=True)
        polarity_counts = defaultdict(int, {"positive": 0, "negative": 0, "neutral": 0})

        # วนลูปเพื่อนับจำนวนรีวิวแต่ละประเภทความรู้สึก
        for polarity in review_data:
            if polarity:  # ตรวจสอบว่าค่ามีอยู่หรือไม่
                polarity_counts[polarity] += 1

        # คำนวณ polarity_percentages
        total_reviews = sum(polarity_counts.values())
        if total_reviews == 0:
            polarity_percentages = {"positive": 0, "negative": 0, "neutral": 0}
        else:
            polarity_percentages = {
                key: (count / total_reviews) * 100
                for key, count in polarity_counts.items()
            }

        # ดึงคะแนนเฉลี่ยของสินค้า
        average_rating = Review.get_average_rating(product)

        # นับจำนวนสินค้าที่ขายไปแล้ว
        sold_count = product.order_items.filter(order__status='completed').aggregate(
            total_sold=Sum('quantity')
        )["total_sold"] or 0

        context.update({
            "images": images,
            "total_reviews": total_reviews,
            "polarity_percentages": polarity_percentages,
            "average_rating": average_rating,
            "sold_count": sold_count,
        })

        return context

class ProductOptionView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs["pk"])
        color = request.GET.get("color", '').strip()
        size = request.GET.get("size", '').strip()

        options = product.options.all()

        # ดึงสีและไซส์ทั้งหมดที่ไม่ซ้ำกัน
        all_colors = options.values_list("color", flat=True).distinct()
        all_sizes = options.values_list("size", flat=True).distinct()

        # ไซส์ที่มีสำหรับสีที่เลือก
        available_sizes = all_sizes # เริ่มต้นให้ไซส์ที่ใช้ได้คือทั้งหมด
        if color:
            available_sizes = list(options.filter(color=color).values_list("size", flat=True).distinct())

        # สีที่มีสำหรับไซส์ี่เลือก
        available_colors = all_colors
        if size:
            available_colors = list(options.filter(size=size).values_list("color", flat=True).distinct())

        # ดึงราคาต่ำสุดและสูงสุดของสินค้า เมื่อมีการกดเลือกยังไม่ครบ 2 อย่างต้องแสดงอันนี้
        price_range = options.aggregate(min_price=Min('price'), max_price=Max('price'))
        min_price = price_range['min_price'] or 0
        max_price = price_range['max_price'] or 0

        # หาราคาและ id ของตัวเลือกที่เลือกจากทั้ง 2 อย่าง
        product_option_id = None
        price = None
        if color and size:
            selected_option = options.filter(color=color, size=size).first()
            if selected_option:
                product_option_id = selected_option.id
                price = selected_option.price

        # ถ้ายังไม่มีการเลือกทั้ง 2 อย่าง ให้ใช้ช่วงราคาสินค้า
        if price is None:
            price = min_price if min_price == max_price else f"{min_price} - {max_price}"

        return render(request, 'shop/partials/product_options.html', {
            "product_id": product.id,
            "product_option_id": product_option_id,
            "all_colors": all_colors,
            "all_sizes": all_sizes,
            "available_colors": available_colors,
            "available_sizes": available_sizes,
            "selected_color": color,
            "selected_size": size,
            "price": price,
        })

class ReviewListView(ListView):
    model = Review
    template_name = "shop/partials/review_list.html"
    context_object_name = "reviews"
    paginate_by = 5

    def get_queryset(self):
        product_id = self.kwargs.get("product_id")
        return Review.objects.filter(product_id=product_id).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_id"] = self.kwargs.get("product_id")  #  ส่ง id ไปที่ template ใช้
        return context
