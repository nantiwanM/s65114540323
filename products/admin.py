from django.contrib import admin
from .models import Product, ProductOption, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 4  # จำนวนฟิลด์เริ่มต้นเมื่อเพิ่มรูปใหม่
    max_num = 4  # จำกัดจำนวนรูปภาพเพิ่มเติมได้ไม่เกิน 4 รูป


class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1  # จำนวนฟิลด์เริ่มต้นเมื่อเพิ่มตัวเลือกสินค้าใหม่


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'category')
    inlines = [ProductImageInline, ProductOptionInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'category', 'cover_image'),
        }),

    )


@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'color', 'size', 'price')
    list_filter = ('product', 'color', 'size')
    search_fields = ('product__name', 'color', 'size')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    list_filter = ('product',)
    search_fields = ('product__name',)
