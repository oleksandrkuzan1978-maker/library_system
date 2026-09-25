from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import DateField


# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    birth_date = models.DateField(verbose_name="Дата рождения")
    profile = models.URLField(blank=True, verbose_name="Ссылка на профиль")
    deleted = models.BooleanField(default=False, verbose_name="Удалён ли автор",
                                  help_text="Если False - автор активен. Если True - автора \
     больше нет в списке доступных")

    rating = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Рейтинг автора")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.TextChoices):
    FICTION = 'fiction', 'Fiction'
    NON_FICTION = 'non-fiction', 'Non-Fiction'
    SCIENCE_FICTION = 'science fiction', 'Science Fiction'
    FANTASY = 'fantasy', 'Fantasy'
    MYSTERY = 'mystery', 'Mystery'
    BIOGRAPHY = 'biography', 'Biography'
    OTHER = 'other', 'Other'


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author, related_name='authors')
    pub_date = DateField()
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=50, choices=Genre, default=Genre.OTHER)
    page_count = models.IntegerField(null=True, blank=True,
                                     validators=[MaxValueValidator(10000)])
    publish = models.ForeignKey('Member', null=True, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,
                                 null=True, related_name='category')
    libraries = models.ManyToManyField('Library', related_name='books')


    def __str__(self):
        return f'{self.title} {self.authors} {self.genre}'


# class Publisher(models.Model):
#     name = models.CharField(max_length=100)
#     address = models.CharField(max_length=255, blank=True)
#     city = models.CharField(max_length=100, blank=True)
#     country = models.CharField(max_length=100)
#
#     def __str__(self):
#         return f'{self.name}'


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f'{self.name}'


class Library(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    site = models.URLField(blank=True, verbose_name='Сайт Библиотеки')

    def __str__(self):
        return f'{self.name}'


class Gender(models.TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'


class Role(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    EMPLOYEE = 'employee', 'Employee'
    READER = 'reader', 'Reader'


class Member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=50, choices=Gender)
    birth_date = models.DateField()
    age = models.IntegerField(validators=[MinValueValidator(6), MaxValueValidator(120)])
    role = models.CharField(max_length=20, choices=Role)
    active = models.BooleanField(default=True)
    libraries = models.ManyToManyField('Library', related_name='members')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


