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
    audio_parts = BookAudioPartSerializer(many=True, read_only=True)
    page_ranges = PageRangeSerializer(many=True, read_only=True)

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
        ]

class BookCategorySerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = BookCategory
        fields = ['id', 'title', 'description', 'books']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
