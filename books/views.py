from rest_framework import viewsets
from .models import BookCategory, Book, BookAudioPart, PageRange, Category
from .serializers import BookCategorySerializer, BookSerializer, BookAudioPartSerializer, PageRangeSerializer, CategorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import cloudinary.uploader
class BookCategoryViewSet(viewsets.ModelViewSet):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer
    http_method_names = ['get', 'post']  # пока без patch и delete

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    http_method_names = ['get', 'post']
    @action(detail=True, methods=['post'], url_path='upload_pdf')
    def upload_pdf(self, request, pk=None):
        pdf_file = request.FILES.get('pdf_file')
        if not pdf_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        upload_result = cloudinary.uploader.upload(
            pdf_file,
            resource_type='raw',
            folder='books_pdfs/'
        )
        
        book = self.get_object()
        book.pdf_url = upload_result['secure_url']
        book.save()
        
        return Response({"pdf_url": book.pdf_url})

class BookAudioPartViewSet(viewsets.ModelViewSet):
    queryset = BookAudioPart.objects.all()
    serializer_class = BookAudioPartSerializer
    http_method_names = ['get', 'post']

class PageRangeViewSet(viewsets.ModelViewSet):
    queryset = PageRange.objects.all()
    serializer_class = PageRangeSerializer
    http_method_names = ['get', 'post']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post']
