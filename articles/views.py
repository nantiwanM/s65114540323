import os

from django.db import transaction
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .models import Article
from .forms import ArticleForm
from django.db.models import F


# ส่วนของแอดมิน

def delete_file(file_path):
    # ตรวจสอบว่าไฟล์ที่ต้องการลบมีอยู่จริงในระบบไฟล์หรือไม่
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error while deleting file: {e}")

class ArticleListView(LoginRequiredMixin, ListView):
    login_url = 'admin_login'
    model = Article
    template_name = 'article/admin/article_list.html'
    paginate_by = 10 # แบ่งหน้า 10 รายการ

    def get_queryset(self):
        # รับค่าค้นหาจาก URL
        query = self.request.GET.get('search', '').strip()  # กรณีที่ไม่มีคำค้นหาจะเป็นค่าว่าง และตัดช่องว่างหัวท้ายออก
        category = self.request.GET.get('category', '')

        articles = Article.objects.all().order_by('-id')  # จัดเรียงจากใหม่ไปเก่า

        # กรองข้อมูลตามคำค้นหาและหมวดหมู่
        if query:
            articles = articles.filter(title__icontains=query)
        if category and category in dict(Article.CATEGORY_CHOICES):
            articles = articles.filter(category=category)

        return articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query_params = self.request.GET.copy()  # คัดลอก query parameters
        query_params.pop('page', None)  # ลบพารามิเตอร์ 'page'

        context['selected_category'] = self.request.GET.get('category', '')
        context['category_choices'] = Article.CATEGORY_CHOICES  # ส่ง Choices ไปที่ Template
        context['query_params'] = query_params.urlencode()  # แปลงเป็น query string ที่ใช้ใน URL

        return context

class ArticleCreateView(LoginRequiredMixin, CreateView):
    login_url = 'admin_login'
    model = Article
    form_class = ArticleForm
    template_name = 'article/admin/article_create.html'
    success_url = reverse_lazy('article_list')

    @transaction.atomic
    def form_valid(self, form):
        form.instance.user = self.request.user  # กำหนด user จากที่ล็อกอินอยู่
        messages.success(self.request, f'เพิ่มบทความ "{form.instance.title}" สำเร็จ!')
        return super().form_valid(form) # บันทึกข้อมูลและ redirect ไปยัง success_url

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'admin_login'
    model = Article
    form_class = ArticleForm
    template_name = 'article/admin/article_edit.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        messages.success(self.request, f"แก้ไขบทความ '{form.instance.title}' สำเร็จ!")
        return super().form_valid(form)

class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'admin_login'
    model = Article

    def post(self, request, *args, **kwargs):
        # ดึงข้อมูลบทความที่ต้องการลบ
        article = self.get_object()

        # ลบรูปภาพปกของบทความ (image) ออกจากระบบไฟล์ (filesystem) ของเซิร์ฟเวอร์
        # เรียกฟังก์ชัน delete_file เพื่อลบไฟล์รูปภาพบทความ
        delete_file(article.image.path)

        # ลบบทความออกจากฐานข้อมูล
        article.delete()

        messages.success(self.request, 'ลบข้อมูลบทความสำเร็จ!')
        return JsonResponse({'status': 'success'}, status=200)




# ส่วนของผู้ใช้

class ShopArticleListView(ListView):
    model = Article
    template_name = 'article/user/article_list.html'
    context_object_name = 'articles'
    ordering = ['-created_at']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query_params = self.request.GET.copy()  # คัดลอก query parameters
        query_params.pop('page', None)  # ลบพารามิเตอร์ 'page' ถ้ามีอยู่ เพื่อป้องกันค่าหน้าเก่าถูกส่งไป

        context['query_params'] = query_params.urlencode()  # แปลงเป็น query string ที่ใช้ใน URL

        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article/user/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_key = f'viewed_article_{self.object.pk}' # กำหนดคีย์ของ session เพื่อเก็บสถานะว่าผู้ใช้เคยดูบทความนี้หรือยัง

        if not self.request.session.get(session_key, False):
            # ถ้ายังไม่เคยดูบทความนี้ ให้เพิ่มจำนวน views
            # ใช้ F('views') + 1 เพื่อเพิ่มค่า views โดยตรงในฐานข้อมูล
            # ป้องกัน Race Condition ที่อาจเกิดจากหลายคำขอพร้อมกัน
            Article.objects.filter(pk=self.object.pk).update(views=F('views') + 1)
            self.request.session[session_key] = True

        return context

