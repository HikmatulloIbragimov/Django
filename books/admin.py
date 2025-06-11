from django.contrib import admin
from .models import Book, BookCategory, BookAudioPart

admin.site.register(Book)
admin.site.register(BookCategory)
admin.site.register(BookAudioPart)