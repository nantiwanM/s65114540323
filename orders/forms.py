from django import forms
from .models import Order
from .models import Order, OrderItem

class OrderFilterForm(forms.Form):
    STATUS_CHOICES = [('', '--- สถานะทั้งหมด ---')] + list(Order.STATUS)

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-md w-full',
            'placeholder': 'ค้นหา หมายเลขคำสั่งซื้อ, ชื่อ, เบอร์โทร',
            'type': 'search'
        })
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'border border-gray-300 bg-white px-4 py-2 pr-10 rounded-md text-gray-700 w-full'
        })
    )

    date_from = forms.DateField(
        required=False,
        label='จากวันที่',
        widget=forms.DateInput(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-md w-full text-gray-700',
            'type': 'date'
        })
    )

    date_to = forms.DateField(
        required=False,
        label='ถึงวันที่',
        widget=forms.DateInput(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-md w-full text-gray-700',
            'type': 'date'
        })
    )

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'address', 'payment_method', 'payment_image']
