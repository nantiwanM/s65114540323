from django import forms
from tinymce.widgets import TinyMCE
from .models import Article

class ArticleForm(forms.ModelForm):

    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-400 rounded-lg',
            'name': 'title',

        })
    )

    # ใช้ TinyMCE widget สำหรับฟิลด์ content
    content = forms.CharField(
        widget=TinyMCE(attrs={
            'class': 'w-full p-2 border border-gray-400 rounded-lg',
            'name': 'content',
        })
    )

    category = forms.ChoiceField(
        choices=[('lifestyle', 'ไลฟ์สไตล์'), ('news', 'ข่าวสาร'), ('recommendatons', 'แนะนำสินค้า')],
        widget=forms.Select(attrs={
            'class': 'w-full p-2 border border-gray-400 rounded-lg',
            'name': 'category',
        })
    )

    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'file-input file-input-bordered file-input-sm w-full max-w-xs mt-2',
            'accept': '.jpg, .jpeg, .png',
            'onchange': "previewImage(event, 'image_preview', 'placeholder_text')",
            'name': 'image',
        })
    )

    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'image']


