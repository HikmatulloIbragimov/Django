from rest_framework import viewsets
from .models import BookCategory, Book, BookAudioPart, PageRange, Category
from .serializers import BookCategorySerializer, BookSerializer, BookAudioPartSerializer, PageRangeSerializer, CategorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from google.cloud import storage
import mimetypes
from django.conf import settings
storage_client = storage.Client(credentials=settings.GS_CREDENTIALS)
class BookCategoryViewSet(viewsets.ModelViewSet):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer
    http_method_names = ['get', 'post', 'put', 'delete']  # пока без patch и delete

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    @action(detail=True, methods=['post'], url_path='upload_pdf')
    def upload_pdf(self, request, pk=None):
        try:
            print("📥 Запрос получен на upload_pdf")
            book = self.get_object()
            print(f"📚 Найдена книга: {book.title} (ID: {book.id})")

            file = request.FILES.get('file')

            if not file:
                print("⚠️ Файл не найден в request.FILES")
                return Response({"error": "Файл не найден"}, status=status.HTTP_400_BAD_REQUEST)

            book = self.get_object()
            print(f"📄 Имя файла: {file.name}")
            bucket_name = 'my-django-buckets'
            blob_path = f"books_pdfs/book_{book.id}/{file.name}"
            print(f"📁 Путь к blob: {blob_path}")

            storage_client = storage.Client(credentials=settings.GS_CREDENTIALS)
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_path)
            blob.upload_from_file(file, content_type=file.content_type)
            print("✅ Файл успешно загружен в Google Cloud Storage")

            # Публичная ссылка
            public_url = f"https://storage.googleapis.com/{bucket_name}/{blob_path}"
            print(f"🌐 Публичная ссылка: {public_url}")
            # Если у Book есть поле под PDF — сохранить ссылку
            book.pdf_url = public_url  # замените на нужное поле, если есть
            book.save()
            print("📌 Ссылка сохранена в модель Book")

            return Response({"message": "Файл успешно загружен", "url": public_url}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @action(detail=True, methods=['post'], url_path='upload_image')
    def upload_image(self, request, pk=None):
        try:
            print("📥 Запрос получен на upload_image")
            book = self.get_object()
            file = request.FILES.get('file')

            if not file:
                return Response({"error": "Файл не найден"}, status=status.HTTP_400_BAD_REQUEST)

            allowed_types = ['image/jpeg', 'image/png', 'image/svg+xml']
            if file.content_type not in allowed_types:
                return Response({"error": "Недопустимый тип файла"}, status=status.HTTP_400_BAD_REQUEST)

            bucket_name = settings.GS_BUCKET_NAME
            blob_path = f"cover_images/book_{book.id}/{file.name}"

            storage_client = storage.Client(credentials=settings.GS_CREDENTIALS)
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_path)
            blob.upload_from_file(file, content_type=file.content_type)

            public_url = f"https://storage.googleapis.com/{bucket_name}/{blob_path}"
            book.cover_image = public_url
            book.save()

            print(f"✅ Картинка загружена: {public_url}")
            return Response({"message": "Изображение успешно загружено", "url": public_url}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"❌ Ошибка загрузки изображения: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class BookAudioPartViewSet(viewsets.ModelViewSet):
    queryset = BookAudioPart.objects.all()
    serializer_class = BookAudioPartSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

class PageRangeViewSet(viewsets.ModelViewSet):
    queryset = PageRange.objects.all()
    serializer_class = PageRangeSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'put', 'delete']
