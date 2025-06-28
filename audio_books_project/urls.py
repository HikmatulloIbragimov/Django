from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),  # 🔥 Убираем 'api/', чтобы /books/ и др. были в корне
]

# Поддержка медиа-файлов (например, изображений баннеров)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
