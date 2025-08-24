from django import template
from cart.models import Cart  # นำเข้า Model Cart

register = template.Library()

@register.filter
def cart_count(user):
    """ ดึงจำนวนสินค้าทั้งหมดในรถเข็นของผู้ใช้ """
    if user.is_authenticated:  # ถ้าผู้ใช้ล็อกอิน
        cart = Cart.objects.filter(user=user).first()
        return cart.get_total_quantity() if cart else 0  # ใช้ get_total_quantity() จาก Model
    return 0  # ถ้าไม่ได้ล็อกอิน คืนค่า 0
