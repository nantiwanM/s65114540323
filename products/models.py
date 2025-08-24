from django.db import models
from django.core.validators import FileExtensionValidator

# ฟังก์ชันสำหรับกำหนดเส้นทางการอัปโหลดรูปภาพสินค้า
def upload_to(instance, filename):
    return f"product/{instance.category}/{filename}"

# ฟังก์ชันสำหรับกำหนดเส้นทางการอัปโหลดรูปภาพเพิ่มเติมของสินค้า
def upload_gallery(instance, filename):
    product_id = instance.product.id if instance.product.id else "0"
    return f"product/gallery/{product_id}_{filename}"


# ตารางสินค้า
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('blouse', 'เสื้อเบล้าส์'),
        ('dress', 'ชุดเดรส'),
        ('jacket', 'แจ็คเก็ต'),
        ('jeans', 'ยีนส์'),
        ('shirt', 'เสื้อเชิ้ต'),
        ('tshirt', 'เสื้อยืด'),
        ('shorts', 'กางเกงขาสั้น'),
        ('skirt', 'กระโปรง'),
    ]

    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    cover_image = models.ImageField(
        upload_to=upload_to,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png'],
                message="กรุณาอัปโหลดไฟล์ที่มีนามสกุล .jpg, .jpeg, หรือ .png เท่านั้น"
            )
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ({self.category})"

    class Meta:
        verbose_name = "สินค้า"
        verbose_name_plural = "สินค้าทั้งหมด"

# ตารางตัวเลือกสินค้า
class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="options")
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    price = models.PositiveIntegerField()

    class Meta:
        verbose_name = "ตัวเลือกสินค้า"
        verbose_name_plural = "ตัวเลือกสินค้าทั้งหมด"

    def __str__(self):
        return f"{self.product.name} - {self.color} - {self.size}"

# ตารางรูปภาพสินค้าเพิ่มเติม
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_gallery)

    class Meta:
        verbose_name = "รูปภาพสินค้าเพิ่มเติม"
        verbose_name_plural = "รูปภาพสินค้าเพิ่มเติมทั้งหมด"

    def __str__(self):
        return f"{self.product.name} - {self.image}"
