from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.views.generic import ListView
from django.views import View

from products.models import Product, ProductOption
from .models import Cart, CartItem

class CartDetailView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = CartItem
    template_name = "cart/cart_detail.html"
    context_object_name = "items"

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart.items.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = Cart.objects.get(user=self.request.user)
        return context

class AddToCartView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, product_id):
        # ดึงข้อมูล Product ที่เกี่ยวข้องกับ product_id
        product = get_object_or_404(Product, id=product_id)

        option_id = request.POST.get("option_id")
        quantity = int(request.POST.get("quantity", 1))

        # ดึงข้อมูล ProductOption โดยใช้ option_id
        product_option = get_object_or_404(ProductOption, id=option_id)

        # ดึงรถเข็นของผู้ใช้หรือสร้างใหม่ถ้าไม่มี
        cart, created = Cart.objects.get_or_create(user=request.user)

        # ตรวจสอบว่าสินค้าอยู่ในตะกร้าหรือยัง
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            product_option=product_option,
            defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        # แจ้งเตือนว่าเพิ่มสินค้าในตะกร้าสำเร็จ
        messages.success(request, "เพิ่มสินค้าลงรถเข็นเรียบร้อยแล้ว!")

        # เปลี่ยนเส้นทางกลับไปยังหน้ารายละเอียดสินค้าหรือหน้าก่อนหน้า
        return redirect('product_detail', pk=product_id)

class UpdateCartView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, pk):
        item = get_object_or_404(CartItem, id=pk, cart__user=request.user)
        action = request.POST.get("action")

        if action == "increase":
            item.quantity += 1
        elif action == "decrease" and item.quantity > 1:
            item.quantity -= 1

        item.save()

        # คำนวณราคารวมของสินค้าและรถเข็นทั้งหมด
        cart = item.cart # ดึงข้อมูลรถเข็นที่เกี่ยวข้องกับ CartItem นั้น ๆ
        total_price = item.item_price()
        cart_total = cart.get_total_price()

        return JsonResponse({
            "quantity": item.quantity,
            "item_total": total_price,
            "cart_total": cart_total
        })

class RemoveCartItemView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, pk):
        # ค้นหาสินค้าในตะกร้าโดยใช้ ID และตรวจสอบว่าเป็นของผู้ใช้ที่ล็อกอิน
        item = get_object_or_404(CartItem, id=pk, cart__user=request.user)
        item.delete()
        return redirect("cart_detail")




