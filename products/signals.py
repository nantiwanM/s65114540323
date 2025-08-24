from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
#import os
from .models import Product, ProductImage

# @receiver(pre_save, sender=Product)
# def delete_old_cover_image(sender, instance, **kwargs):
#     # ตรวจสอบว่ามี Primary Key (หมายถึงเป็นการอัปเดต ไม่ใช่การสร้างใหม่)
#     if instance.pk:
#         try:
#             old_instance = Product.objects.get(pk=instance.pk)
#             # ตรวจสอบว่า cover_image เปลี่ยนไปหรือไม่
#             if old_instance.cover_image and old_instance.cover_image != instance.cover_image:
#                 # ลบไฟล์เก่าถ้ามีอยู่
#                 old_cover_image_path = old_instance.cover_image.path
#                 if os.path.isfile(old_cover_image_path):
#                     os.remove(old_cover_image_path)
#         except ObjectDoesNotExist:
#             pass  # หากไม่มี instance เก่า ไม่ต้องทำอะไร

# @receiver(pre_save, sender=ProductImage)
# def delete_old_product_image(sender, instance, **kwargs):
#     # ตรวจสอบว่าเป็นการอัปเดต ไม่ใช่การสร้างใหม่
#     if instance.pk:
#         try:
#             old_instance = ProductImage.objects.get(pk=instance.pk)
#             # ตรวจสอบว่า image เปลี่ยนไปหรือไม่
#             if old_instance.image and old_instance.image != instance.image:
#                 # ลบไฟล์เก่าถ้ามีอยู่
#                 old_image_path = old_instance.image.path
#                 if os.path.isfile(old_image_path):
#                     os.remove(old_image_path)
#         except ObjectDoesNotExist:
#             pass

# =========================
# Pre-save: ลบไฟล์เก่าก่อนอัปเดต สำหรับ Cloudinary
# =========================
@receiver(pre_save, sender=Product)
def delete_old_cover_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Product.objects.get(pk=instance.pk)
            if old_instance.cover_image and old_instance.cover_image != instance.cover_image:
                try:
                    old_instance.cover_image.delete(save=False)
                except Exception as e:
                    print(f"Could not delete old cover image: {e}")
        except ObjectDoesNotExist:
            pass

@receiver(pre_save, sender=ProductImage)
def delete_old_product_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = ProductImage.objects.get(pk=instance.pk)
            if old_instance.image and old_instance.image != instance.image:
                try:
                    old_instance.image.delete(save=False)
                except Exception as e:
                    print(f"Could not delete old product image: {e}")
        except ProductImage.DoesNotExist:
            pass


# =========================
# Post-delete: ลบไฟล์จาก Cloudinary เมื่อ object ถูกลบ
# =========================
@receiver(post_delete, sender=Product)
def delete_cover_image_on_delete(sender, instance, **kwargs):
    if instance.cover_image:
        try:
            instance.cover_image.delete(save=False)
        except Exception as e:
            print(f"Could not delete cover image on delete: {e}")

@receiver(post_delete, sender=ProductImage)
def delete_product_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        try:
            instance.image.delete(save=False)
        except Exception as e:
            print(f"Could not delete product image on delete: {e}")