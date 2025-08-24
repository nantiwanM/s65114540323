from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
import os
from .models import Product, ProductImage

@receiver(pre_save, sender=Product)
def delete_old_cover_image(sender, instance, **kwargs):
    # ตรวจสอบว่ามี Primary Key (หมายถึงเป็นการอัปเดต ไม่ใช่การสร้างใหม่)
    if instance.pk:
        try:
            old_instance = Product.objects.get(pk=instance.pk)
            # ตรวจสอบว่า cover_image เปลี่ยนไปหรือไม่
            if old_instance.cover_image and old_instance.cover_image != instance.cover_image:
                # ลบไฟล์เก่าถ้ามีอยู่
                old_cover_image_path = old_instance.cover_image.path
                if os.path.isfile(old_cover_image_path):
                    os.remove(old_cover_image_path)
        except ObjectDoesNotExist:
            pass  # หากไม่มี instance เก่า ไม่ต้องทำอะไร

@receiver(pre_save, sender=ProductImage)
def delete_old_product_image(sender, instance, **kwargs):
    # ตรวจสอบว่าเป็นการอัปเดต ไม่ใช่การสร้างใหม่
    if instance.pk:
        try:
            old_instance = ProductImage.objects.get(pk=instance.pk)
            # ตรวจสอบว่า image เปลี่ยนไปหรือไม่
            if old_instance.image and old_instance.image != instance.image:
                # ลบไฟล์เก่าถ้ามีอยู่
                old_image_path = old_instance.image.path
                if os.path.isfile(old_image_path):
                    os.remove(old_image_path)
        except ObjectDoesNotExist:
            pass