from rest_framework import viewsets
from .models import BookCategory, Book, BookAudioPart, PageRange, Category
from .serializers import BookCategorySerializer, BookSerializer, BookAudioPartSerializer, PageRangeSerializer, CategorySerializer
from rest_framework.response import Response
from google.cloud import storage
from .models import ConversationText
from .serializers import ConversationTextSerializer
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
import uuid
import asyncio
from .utils.text_to_audio import text_to_speech_parts
from google.cloud import storage
from django.conf import settings
import tempfile
from pathlib import Path
from asgiref.sync import sync_to_async
from .models import ConversationText
from .serializers import ConversationTextSerializer
from datetime import datetime
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
import fnmatch
from .models import UploadedFile
from .serializers import UploadedFileSerializer
import os
from .models import Banner
from .serializers import BannerSerializer



storage_client = storage.Client(credentials=settings.GS_CREDENTIALS)
class BookCategoryViewSet(viewsets.ModelViewSet):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer
    http_method_names = ['get', 'post', 'put', 'delete']  # пока без patch и delete

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    
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

class ConversationTextViewSet(ModelViewSet):
    queryset = ConversationText.objects.all()
    serializer_class = ConversationTextSerializer

    def perform_create(self, serializer):
        # Сначала сохраняем, чтобы получить ID
        instance = serializer.save()
        asyncio.run(self.generate_audio(instance))  # Генерируем и сохраняем mp3

    def perform_update(self, serializer):
        instance = serializer.save()
        self.delete_gcs_file_by_id(instance.id)  # Удаляем старый mp3
        asyncio.run(self.generate_audio(instance))  # Генерируем новый

    def perform_destroy(self, instance):
        self.delete_gcs_file_by_id(instance.id)  # Удаляем mp3
        instance.delete()  # Удаляем запись из базы

    async def generate_audio(self, instance):
        file_id = str(instance.id)  # Используем ID как имя файла

        tmp_dir = Path(tempfile.gettempdir())
        local_audio_path = str(tmp_dir / f"audio_{file_id}.mp3")

        # Генерация mp3
        await text_to_speech_parts(instance.text, output_path_prefix=local_audio_path.replace(".mp3", ""))

        # Путь внутри бакета
        bucket_name = settings.GS_BUCKET_NAME
        destination_blob_name = f"conversation_audios/{file_id}.mp3"

        client = storage.Client(credentials=settings.GS_CREDENTIALS)
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_audio_path)


        

        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        public_url = f"https://storage.googleapis.com/{bucket_name}/{destination_blob_name}?v={timestamp}"
        instance.audio_url = public_url
        await sync_to_async(instance.save)()

    def delete_gcs_file_by_id(self, instance_id):
        bucket_name = settings.GS_BUCKET_NAME
        client = storage.Client(credentials=settings.GS_CREDENTIALS)
        bucket = client.bucket(bucket_name)

        blob_path = f"conversation_audios/{instance_id}.mp3"
        blob = bucket.blob(blob_path)

        if blob.exists():
            blob.delete()
    def update(self, request, *args, **kwargs):
        print("✅ update() called")

        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        old_text = instance.text

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        new_text = serializer.validated_data.get("text", old_text)
        print("📄 old_text:", old_text)
        print("🆕 new_text:", new_text)

        # Сохраняем обновлённую запись
        self.perform_update(serializer)

        if old_text != new_text:
            print("🔁 Text changed, regenerating audio...")
            self.delete_gcs_file_by_id(instance.id)
            asyncio.run(self.generate_audio(instance))
        else:
            print("⚠️ Text not changed — skipping audio generation.")
        return Response(serializer.data)





class UploadedFileViewSet(viewsets.ModelViewSet):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    http_method_names = ['get', 'post', 'put', 'delete']


class UploadBookFileAPIView(APIView):
    parser_classes = [MultiPartParser]

    def get(self, request):
        client = storage.Client(credentials=settings.GS_CREDENTIALS)
        bucket = client.bucket(settings.GS_BUCKET_NAME)
        blobs = bucket.list_blobs(prefix="books_uploads/")

        files = []
        for blob in blobs:
            blob_name = blob.name
            file_url = f"https://storage.googleapis.com/{settings.GS_BUCKET_NAME}/{blob_name}"
            file_id = os.path.splitext(os.path.basename(blob_name))[0]
            file_type = blob_name.split('/')[1]

            files.append({
                "file_id": file_id,
                "file_type": file_type,
                "file_url": file_url
            })

        return Response(files)

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "Файл обязателен"}, status=400)

        file_type = "image" if file.content_type.startswith("image/") else "pdf"
        ext = file.name.split('.')[-1]
        file_uuid = uuid.uuid4()
        blob_path = f"books_uploads/{file_type}/{file_uuid}.{ext}"

        client = storage.Client(credentials=settings.GS_CREDENTIALS)
        bucket = client.bucket(settings.GS_BUCKET_NAME)
        blob = bucket.blob(blob_path)
        blob.upload_from_file(file, content_type=file.content_type)

        public_url = f"https://storage.googleapis.com/{settings.GS_BUCKET_NAME}/{blob_path}"

        UploadedFile.objects.create(
            id=file_uuid,
            file_url=public_url,
            file_type=file_type
        )

        return Response({
            "file_url": public_url,
            "file_id": str(file_uuid),
            "file_type": file_type
        }, status=201)





class UploadBookFileDetailAPIView(APIView):
    def get(self, request, file_id):
        bucket = storage.Client(credentials=settings.GS_CREDENTIALS).bucket(settings.GS_BUCKET_NAME)

        for file_type in ["pdf", "image"]:
            for ext in ["pdf", "jpg", "jpeg", "png", "svg"]:
                blob_path = f"books_uploads/{file_type}/{file_id}.{ext}"
                blob = bucket.blob(blob_path)
                if blob.exists():
                    public_url = f"https://storage.googleapis.com/{settings.GS_BUCKET_NAME}/{blob_path}"
                    return Response({
                        "file_url": public_url,
                        "file_type": file_type,
                        "extension": ext
                    }, status=200)

        return Response({"error": "Файл не найден"}, status=404)

    def put(self, request, file_id):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "Файл обязателен"}, status=400)

        file_type = "image" if file.content_type.startswith("image/") else "pdf"
        ext = file.name.split('.')[-1]
        blob_path = f"books_uploads/{file_type}/{file_id}.{ext}"

        client = storage.Client(credentials=settings.GS_CREDENTIALS)
        bucket = client.bucket(settings.GS_BUCKET_NAME)
        blob = bucket.blob(blob_path)

        if blob.exists():
            blob.delete()

        blob.upload_from_file(file, content_type=file.content_type)
        public_url = f"https://storage.googleapis.com/{settings.GS_BUCKET_NAME}/{blob_path}"

        UploadedFile.objects.filter(id=file_id).update(file_url=public_url, file_type=file_type)

        return Response({
            "message": "Файл обновлён",
            "file_url": public_url
        }, status=200)

    def delete(self, request, file_id):
        file_type = request.query_params.get("file_type", "pdf")
        prefix = f"books_uploads/{file_type}/{file_id}"

        client = storage.Client(credentials=settings.GS_CREDENTIALS)
        bucket = client.bucket(settings.GS_BUCKET_NAME)

        blobs = list(bucket.list_blobs(prefix=f"books_uploads/{file_type}/"))
        matched = [b for b in blobs if fnmatch.fnmatch(b.name, f"{prefix}.*")]

        if not matched:
            return Response({"error": "Файл не найден"}, status=404)

        for blob in matched:
            blob.delete()

        UploadedFile.objects.filter(id=file_id).delete()

        return Response({"message": "Файл(ы) удалены"}, status=204)


class BannerUploadAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        image = request.FILES.get('image')
        url = request.data.get('url')

        if not image or not url:
            return Response({"error": "Нужны и image, и url"}, status=400)

        # Загружаем картинку в Google Cloud Storage
        ext = image.name.split('.')[-1]
        banner_id = uuid.uuid4()
        path = f"banners/{banner_id}.{ext}"

        bucket = storage.Client(credentials=settings.GS_CREDENTIALS).bucket(settings.GS_BUCKET_NAME)
        blob = bucket.blob(path)
        blob.upload_from_file(image, content_type=image.content_type)
        image_url = f"https://storage.googleapis.com/{settings.GS_BUCKET_NAME}/{path}"

        # Можно сохранить в БД, если нужно (опционально)

        return Response({
            "image": image_url,
            "url": url
        }, status=201)

        
class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer