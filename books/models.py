from django.db import models
import uuid
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name


class BookCategory(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title




class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE, related_name="books")
    cover_image = models.URLField(blank=True)
    pdf_url = models.URLField(blank=True)  # заменили pdf_file на pdf_url
    audio_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    book_author = models.CharField(max_length=255, default="")

class BookAudioPart(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="audio_parts")
    start_page = models.IntegerField()
    end_page = models.IntegerField()
    audio_url = models.URLField(default="", blank=True)

class PageRange(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="page_ranges")
    start_page = models.IntegerField()
    end_page = models.IntegerField()
    audio_url = models.URLField(default="", blank=True)


class ConversationText(models.Model):
    text = models.TextField()
    audio_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]



class UploadedFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_url = models.URLField()
    file_type = models.CharField(max_length=10)  # "pdf" или "image"
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_type.upper()} - {self.id}"


class Banner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_url = models.URLField()
    target_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)