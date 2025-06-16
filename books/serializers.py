from rest_framework import serializers
from .models import Category, BookCategory, Book, BookAudioPart, PageRange

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
    category = serializers.PrimaryKeyRelatedField(queryset=BookCategory.objects.all())  # 👈 возвращает строку из __str__ метода модели BookCategory
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
