from django.contrib import admin
from .models import  Author, Book, Category, Library, Member
# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birth_date')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'pub_date', 'page_count', 'description')


# @admin.register(Publisher)
# class PublisherAdmin(admin.ModelAdmin):
#     list_display = ('name', 'address', 'city')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')