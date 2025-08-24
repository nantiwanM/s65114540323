from django.contrib.auth.models import User
from django.db import models
from accounts.models import UserProfile
from tinymce.models import HTMLField
import os
from django.db.models.signals import pre_save
from django.dispatch import receiver

# ฟังก์ชันสำหรับกำหนดเส้นทางการอัปโหลดรูปภาพของบทความ
def upload_to(instance, filename):
    return f"article/{instance.category}/{filename}"

class Article(models.Model):
    CATEGORY_CHOICES = [
        ('lifestyle', 'ไลฟ์สไตล์'),
        ('news', 'ข่าวสาร'),
        ('recommendatons', 'แนะนำสินค้า'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=255)
    content = HTMLField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to=upload_to)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# @receiver(pre_save, sender=Article)
# def delete_old_image(sender, instance, **kwargs):
#     # ตรวจสอบว่าเป็นการอัปเดตข้อมูล (ไม่ใช่การสร้างใหม่)
#     if instance.pk:
#         try:
#             # ดึงข้อมูลบทความเดิมจากฐานข้อมูล
#             old_article = Article.objects.get(pk=instance.pk)
#             old_image = old_article.image  # ไฟล์รูปภาพเดิม
#             new_image = instance.image  # ไฟล์รูปภาพใหม่ที่กำลังจะบันทึก
#
#             # หากมีการเปลี่ยนแปลงไฟล์รูปภาพ ให้ลบไฟล์รูปภาพเดิมออก
#             if old_image and old_image != new_image:
#                 old_image_path = old_image.path  # เส้นทางไฟล์ของรูปภาพเดิม
#                 if os.path.exists(old_image_path):  # ตรวจสอบว่าไฟล์ยังอยู่หรือไม่
#                     os.remove(old_image_path)  # ลบไฟล์รูปภาพเดิมออกจากระบบ
#         except Article.DoesNotExist:
#             pass  # หากไม่มีบทความเดิม (เป็นการสร้างใหม่) จะไม่มีภาพเก่าให้ลบ
