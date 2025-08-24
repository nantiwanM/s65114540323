from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .models import Article

# ===== ลบภาพเก่าเมื่อมีการอัปเดต สำหรับ Cloudinary =====
@receiver(pre_save, sender=Article)
def delete_old_article_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Article.objects.get(pk=instance.pk)
            if old_instance.image and old_instance.image != instance.image:
                try:
                    old_instance.image.delete(save=False)
                except Exception as e:
                    print(f"Could not delete old article image: {e}")
        except ObjectDoesNotExist:
            pass

# ===== ลบภาพเมื่อบทความถูกลบ สำหรับ Cloudinary =====
@receiver(post_delete, sender=Article)
def delete_article_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        try:
            instance.image.delete(save=False)
        except Exception as e:
            print(f"Could not delete article image on delete: {e}")