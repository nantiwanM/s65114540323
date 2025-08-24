import os

from django.db import transaction
from django.db.models import Min, Max
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Product, ProductOption, ProductImage
from .forms import ProductForm


def save_product_options(product, colors, sizes, prices):
    """
    บันทึกตัวเลือกสินค้า (ProductOption) ลงในฐานข้อมูล
    ตัวอย่าง
    colors = ["Red", "Blue"]
    sizes = ["M", "L"]
    prices = [500, 550]

    รอบที่ 1: color="Red", size="M", price=500
    รอบที่ 2: color="Blue", size="L", price=550
    """
    for color, size, price in zip(colors, sizes, prices):
        ProductOption.objects.create(
            product=product,
            color=color,
            size=size,
            price=price
        )

def delete_file(file_path):
    # ตรวจสอบว่าไฟล์ที่ต้องการลบมีอยู่จริงในระบบไฟล์หรือไม่
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error while deleting file: {e}")

class ProductListView(LoginRequiredMixin, ListView):
    login_url = 'admin_login'
    model = Product
    template_name = "products/product_list.html"
    paginate_by = 10  # แบ่งหน้า 10 รายการ

    def get_queryset(self):
        # รับค่าค้นหาจาก URL
        query = self.request.GET.get('search', '').strip() # กรณีที่ไม่มีคำค้นหาจะเป็นค่าว่าง และตัดช่องว่างหัวท้ายออก
        category = self.request.GET.get('category', '')

        # ดึงข้อมูลสินค้าพร้อมราคาต่ำสุดและสูงสุด
        products = Product.objects.annotate(
            min_price=Min('options__price'),
            max_price=Max('options__price'),
        )

        # กรองข้อมูลตามคำค้นหาและหมวดหมู่
        if query:
            products = products.filter(name__icontains=query)
        if category and category in dict(Product.CATEGORY_CHOICES):
            products = products.filter(category=category)

        # จัดเรียงตาม ID จากล่าสุดไปเก่าสุด
        return products.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query_params = self.request.GET.copy() # คัดลอก query parameters
        query_params.pop('page', None) # ลบพารามิเตอร์ 'page' ถ้ามีอยู่ เพื่อป้องกันค่าหน้าเก่าถูกส่งไป

        context['selected_category'] = self.request.GET.get('category', '')
        context['category_choices'] = Product.CATEGORY_CHOICES  # ส่ง Choices ไปที่ Template
        context['query_params'] = query_params.urlencode()  # แปลงเป็น query string ที่ใช้ใน URL

        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = 'admin_login'
    model = Product
    form_class = ProductForm
    template_name = 'products/product_create.html'
    success_url = reverse_lazy('product_list')

    @transaction.atomic
    def form_valid(self, form):
        # บันทึกสินค้า
        product = form.save()

        # ดึงข้อมูลตัวเลือกสินค้าจากฟอร์ม
        colors = self.request.POST.getlist('color[]')
        sizes = self.request.POST.getlist('size[]')
        prices = self.request.POST.getlist('price[]')

        # บันทึกตัวเลือกสินค้า
        save_product_options(product, colors, sizes, prices)

        # ดึงข้อมูลรูปภาพเพิ่มเติมจากฟอร์ม
        image_files = self.request.FILES.getlist('images[]')

        # บันทึกรูปภาพเพิ่มเติม
        if image_files:
            for image in image_files:
                ProductImage.objects.create(
                    product=product,
                    image=image
                )

        messages.success(self.request, f'เพิ่มสินค้า "{product.name}" สำเร็จ!')
        return super().form_valid(form) # ทำการ redirect ไปยัง success_url

class ProductEditView(LoginRequiredMixin, UpdateView):

    login_url = 'admin_login'
    model = Product
    form_class = ProductForm
    template_name = 'products/product_edit.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        # ดึงข้อมูลตัวเลือกสินค้าและรูปภาพเพิ่มเติมเพื่อแสดงในฟอร์ม
        context = super().get_context_data(**kwargs)
        product = self.object  # ดึงสินค้าที่กำลังแก้ไข
        context['product'] = product  # ส่งสินค้าไปยัง template
        context['options'] = product.options.all()  # ส่งตัวเลือกสินค้า
        images = list(product.images.all())  # แปลง QuerySet เป็น List

        # เติมให้รูปภาพแสดงครบ 4 ช่องในฟอร์ม หากยังมีไม่ครบ
        while len(images) < 4:
            images.append(None)

        context['images'] = images
        return context

    @transaction.atomic
    def form_valid(self, form):
        # 1. ดึงข้อมูลสินค้าจากฟอร์มและทำการอัปเดต
        product = form.save()

        # 2. ลบตัวเลือกสินค้าเก่าทั้งหมดก่อน แล้วจะเพิ่มใหม่
        ProductOption.objects.filter(product=product).delete()

        # ดึงข้อมูลตัวเลือกสินค้าจากฟอร์ม
        colors = self.request.POST.getlist('color[]')
        sizes = self.request.POST.getlist('size[]')
        prices = self.request.POST.getlist('price[]')

        # บันทึกตัวเลือกสินค้าใหม่
        save_product_options(product, colors, sizes, prices)

        # 3. ดึงข้อมูลรูปภาพเพิ่มเติมจากฟอร์ม
        new_images = self.request.FILES.getlist('new_images[]')

        # ถ้ามีรูปภาพใหม่ เพิ่มภาพใหม่ลงในฐานข้อมูล
        if new_images:
            for image in new_images:
                ProductImage.objects.create(
                    product=product,
                    image=image
                )

        messages.success(self.request, f'แก้ไขข้อมูลสินค้า "{product.name}" สำเร็จ!')
        return super().form_valid(form)

class DeleteImageView(View):

    def delete(self, request, image_id):
        # ดึงข้อมูลรูปภาพที่ต้องการลบ
        image = get_object_or_404(ProductImage, id=image_id)

        # ลบรูปภาพออกจากระบบไฟล์
        delete_file(image.image.path)

        # ลบข้อมูลรูปภาพออกจากฐานข้อมูล
        image.delete()

        # ส่ง HTML ใหม่ที่แทนที่ content ของ #images_preview
        return HttpResponse('<span class="text-gray-400">รูปภาพ</span>')  # แสดงข้อความ placeholder

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'admin_login'
    model = Product

    def post(self, request, *args, **kwargs):
        # ดึงข้อมูลสินค้าที่ต้องการลบ
        product = self.get_object()

        # ลบรูปภาพปกของสินค้า (cover_image) ออกจากระบบไฟล์ (filesystem) ของเซิร์ฟเวอร์
        # เรียกฟังก์ชัน delete_file เพื่อลบไฟล์รูปภาพปกสินค้า
        delete_file(product.cover_image.path)

        # ลบรูปภาพที่เกี่ยวข้องจาก ProductImage ออกจากระบบไฟล์ (filesystem) ของเซิร์ฟเวอร์
        product_images = product.images.all()
        for image in product_images:
            delete_file(image.image.path)

        # ลบสินค้าและข้อมูลที่เกี่ยวข้องออกจากฐานข้อมูล
        product.delete()

        messages.success(self.request, 'ลบข้อมูลสินค้าสำเร็จ!')
        return JsonResponse({'status': 'success'}, status=200)


