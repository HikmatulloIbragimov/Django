from rest_framework.routers import DefaultRouter
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import BookViewSet
from .views import (
    BookCategoryViewSet, BookViewSet, BookAudioPartViewSet,
    PageRangeViewSet, CategoryViewSet, ConversationTextViewSet, BannerViewSet
)
from .views import UploadBookFileAPIView, UploadBookFileDetailAPIView , UploadedFileViewSet


router = DefaultRouter()
router.register(r'book-categories', BookCategoryViewSet)
router.register(r'books', BookViewSet)
router.register(r'audio-parts', BookAudioPartViewSet)
router.register(r'page-ranges', PageRangeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'conversation_texts', ConversationTextViewSet)
router.register(r'uploaded-files', UploadedFileViewSet)
router.register(r'banners', BannerViewSet)
urlpatterns = router.urls + [
    path('upload/', UploadBookFileAPIView.as_view(), name='upload-files'),
    path('upload/<uuid:file_id>/', UploadBookFileDetailAPIView.as_view(), name='upload-file-detail')
]



