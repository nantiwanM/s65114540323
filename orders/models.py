from django.db import models
from accounts.models import UserProfile
from products.models import Product
import uuid
from datetime import datetime
from django.utils import timezone


# ฟังก์ชันสำหรับกำหนดเส้นทางการอัปโหลดรูปภาพของสลิปโอนเงิน
def upload_to(instance,filename):
    return f"payments/{instance.id}_{filename}"

class Order(models.Model):
    PaymentMethod = (
        ('slip', 'แนบสลิป'),
    )

    STATUS = (
        ('pending', 'รอการชำระเงิน'),
        ('paid', 'จ่ายแล้ว'),
        ('completed', 'สำเร็จ'),
        ('cancelled', 'ยกเลิก'),
    )

    order_code = models.CharField(max_length=20, unique=True, editable=False) # ไม่แสดงในฟอร์มการสร้างหรือการแก้ไขข้อมูล
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders')
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    address = models.TextField()
    total_price = models.IntegerField()
    payment_method = models.CharField(max_length=50, choices=PaymentMethod)
    payment_image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    order_date = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"หมายเลขคำสั่งซื้อ: {self.order_code} - ชื่อ: {self.full_name} | ราคารวม: {self.total_price} บาท | สถานะ: {self.get_status_display()}"

    def save(self, *args, **kwargs):
        if not self.order_code:
            while True:
                # สร้าง order_code
                unique_part = uuid.uuid4().hex[:8]# ใช้เลขและตัวอักษร 8 หลักจาก UUID
                self.order_code = f"{datetime.now().strftime('%y%m%d')}{unique_part}"
                if not Order.objects.filter(order_code=self.order_code).exists():
                    break
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField()
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    unit_price = models.IntegerField()

    def __str__(self):
        return f"{self.id} | หมายเลขคำสั่งซื้อ: {self.order.order_code} | สินค้า: {self.product.name} - จำนวน: {self.quantity} | สี: {self.color} | ขนาด: {self.size} | ราคาต่อหน่วย: {self.unit_price} บาท"

    # จะถูกเรียกใช้งานได้เหมือนฟิลด์ (attribute) แทนที่จะเป็นฟังก์ชัน
    @property
    def total_price(self):
        return self.quantity * self.unit_price

