from rest_framework.routers import DefaultRouter
from .views import BookCategoryViewSet, BookViewSet, BookAudioPartViewSet, PageRangeViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'book-categories', BookCategoryViewSet)
router.register(r'books', BookViewSet)
router.register(r'audio-parts', BookAudioPartViewSet)
router.register(r'page-ranges', PageRangeViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = router.urls


