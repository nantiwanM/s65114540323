from django.contrib import admin
from orders.models import Order, OrderItem
from django.utils.html import format_html

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_code', 'product', 'quantity', 'color', 'size', 'unit_price', 'total_price')
    search_fields = ('product__name', 'order__order_code')  # เพิ่มช่องค้นหา

    def order_code(self, obj):
        return obj.order.order_code

    order_code.short_description = 'หมายเลขคำสั่งซื้อ'

    def total_price(self, obj):
        return obj.quantity * obj.unit_price
    total_price.short_description = 'ราคารวม'

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_code', 'full_name', 'total_price', 'colored_status', 'order_date')

    def colored_status(self, obj):
        color_map = {
            'pending': 'orange',
            'paid': 'blue',
            'completed': 'green',
            'cancelled': 'red',
        }
        color = color_map.get(obj.status, 'gray')  # สี default ถ้าไม่ตรงกับเงื่อนไข
        return format_html(
            '<span style="background-color: {}; padding: 5px; border-radius: 5px; color: white;">{}</span>',
            color,
            obj.get_status_display()
        )
    colored_status.short_description = 'สถานะ'

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)