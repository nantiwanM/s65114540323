from django.db import models

from accounts.models import UserProfile
from products.models import Product, ProductOption


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    # รวมราคาสินค้าทั้งหมดใน cart ของ user นั้นๆ
    def get_total_price(self):
        return sum(item.item_price() for item in self.items.all())

    # รวมจำนวนสินค้าทั้งหมด
    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} : {self.cart.id} | {self.product_option.product.name} - {self.product_option.color} / {self.product_option.size} ({self.quantity})"

    # คำนวณราคารวมของแต่ละสินค้า
    def item_price(self):
        return self.product_option.price * self.quantity
