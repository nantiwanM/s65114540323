"""
URL configuration for CNStyleShop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),

    path('dj-admin/', admin.site.urls),

    path('', include('shop.urls')),

    path('cart/', include('cart.urls')),

    path('account/', include('accounts.urls')),

    path('admin/', include('products.urls')),

    path('', include('articles.urls')), # มีทั้งส่วนของแอดมินและผู้้ใช้

    path('', include('orders.urls')), # มีทั้งส่วนของแอดมินและผู้้ใช้

    path('admin/', include('dashboard.urls')),
]

# เสริมสำหรับเสิร์ฟ Media Files ในโหมด Development
if settings.DEBUG:
    # สำหรับ media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # สำหรับ django-browser-reload
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]