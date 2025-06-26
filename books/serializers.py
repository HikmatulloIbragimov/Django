from rest_framework import serializers
from .models import Category, BookCategory, Book, BookAudioPart, PageRange 
from .models import ConversationText
from .models import UploadedFile
from .models import Banner


class BookAudioPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAudioPart
        fields = ['id', 'book', 'start_page', 'end_page', 'audio_url']


class PageRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageRange
        fields = ['id', 'book', 'start_page', 'end_page', 'audio_url']

class BookSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    audio_parts = BookAudioPartSerializer(many=True, read_only=True)
    page_ranges = PageRangeSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()  # 👈 возвращает строку из __str__ метода модели BookCategory
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'description',
            'category',
            'cover_image',
            'pdf_url',
            'audio_required',
            'created_at',
            'audio_parts',
            'page_ranges',
            'price',
            'book_author',
        ]

class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = ['id', 'title', 'description']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']




class ConversationTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationText
        fields = ['id', 'text', 'audio_url', 'created_at']


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'file_type', 'file_url', 'uploaded_at']

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'image_url', 'target_url', 'created_at']