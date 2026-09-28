"""Модели библиотек, книг, участников, выдач, отзывов и событий."""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import DateField
from django.utils import timezone
# from django.db.models import Avg


# Create your models here.

class Author(models.Model):
    """Автор книг с персональными данными, рейтингом и признаком удаления."""
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
        """Вернуть имя и фамилию автора."""
        return f"{self.first_name} {self.last_name}"


class Genre(models.TextChoices):
    """Допустимые литературные жанры книг."""
    FICTION = 'fiction', 'Fiction'
    NON_FICTION = 'non-fiction', 'Non-Fiction'
    SCIENCE_FICTION = 'science fiction', 'Science Fiction'
    FANTASY = 'fantasy', 'Fantasy'
    MYSTERY = 'mystery', 'Mystery'
    BIOGRAPHY = 'biography', 'Biography'
    OTHER = 'other', 'Other'


class Book(models.Model):
    """Книга, связанная с авторами, категорией, библиотеками и отзывами."""
    title = models.CharField(max_length=100, verbose_name='Название')
    authors = models.ManyToManyField(Author, related_name='authors', verbose_name='Авторы')
    pub_date = DateField(verbose_name='Дата публикации', blank=True, null=True,)
    description = models.TextField(blank=True, verbose_name='Описание')
    genre = models.CharField(max_length=50, choices=Genre, default=Genre.OTHER, verbose_name='Жанр')
    page_count = models.IntegerField(null=True, blank=True,
                                     validators=[MaxValueValidator(10000)], verbose_name='Количество страниц')
    publish = models.ForeignKey('Member', null=True, on_delete=models.CASCADE
                                , verbose_name='Участник, связанный с публикацией')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,
                                 null=True, related_name='category', verbose_name='Категория')
    libraries = models.ManyToManyField('Library', related_name='books', verbose_name='Библиотеки')

    @property
    def rating(self):
        """Вернуть среднюю оценку с округлением до двух знаков или 0 без отзывов."""
        reviews = self.reviews.all()
        total_reviews = reviews.count()
        if total_reviews == 0:
            return 0
        total_rating = sum(review.rating for review in reviews)
        average_rating = total_rating / total_reviews
        return round(average_rating, 2)
    # @property
    # def rating(self):
    #     """Вернуть среднюю оценку книги или None, если оценок нет."""
    #     average = self.reviews.aggregate(average_rating=Avg('rating'))['average_rating']
    #     return round(average, 2) if average is not None else None

    def __str__(self):
        """Вернуть название, строковое представление менеджера авторов и жанр."""
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
    """Категория книг с уникальным названием."""
    name = models.CharField(max_length=30, unique=True, verbose_name='Название')

    def __str__(self):
        """Вернуть название категории."""
        return f'{self.name}'


class Library(models.Model):
    """Библиотека с названием, местоположением и необязательным сайтом."""
    name = models.CharField(max_length=100, verbose_name='Название')
    location = models.CharField(max_length=200, verbose_name='Местоположение')
    site = models.URLField(blank=True, verbose_name='Сайт Библиотеки')

    def __str__(self):
        """Вернуть название библиотеки."""
        return f'{self.name}'


class Gender(models.TextChoices):
    """Допустимые значения пола участников и авторов."""
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'


class Role(models.TextChoices):
    """Роли участников библиотеки: администратор, сотрудник и читатель."""
    ADMIN = 'admin', 'Admin'
    EMPLOYEE = 'employee', 'Employee'
    READER = 'reader', 'Reader'


class Member(models.Model):
    """Участник библиотек с персональными данными, ролью и признаком активности."""
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    gender = models.CharField(max_length=50, choices=Gender, verbose_name='Пол')
    birth_date = models.DateField(verbose_name='Дата рождения')
    age = models.IntegerField(validators=[MinValueValidator(6), MaxValueValidator(120)]
                              , verbose_name='Возраст')
    role = models.CharField(max_length=20, choices=Role, verbose_name='Роль')
    active = models.BooleanField(default=True, verbose_name='Активен')
    libraries = models.ManyToManyField('Library', related_name='members', verbose_name='Библиотеки')

    def __str__(self):
        """Вернуть имя и фамилию участника."""
        return f'{self.first_name} {self.last_name}'


class Posts(models.Model):
    """Публикация участника для библиотеки с датами и признаком модерации."""
    title = models.CharField(max_length=255, unique_for_date='created_at', verbose_name='Заголовок публикации')
    body = models.TextField(verbose_name='Текст публикации')
    author = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')
    moderated = models.BooleanField(default=False, verbose_name='Прошла модерацию')
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='posts'
                                , verbose_name='Библиотека')
    created_at = models.DateField(verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        """Вернуть заголовок публикации и её автора."""
        return f'{self.title} {self.author}'


class Borrow(models.Model):
    """Выдача книги участнику библиотеки со сроком и признаком возврата."""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='borrows'
                               , verbose_name='Участник')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrows', verbose_name='Книга')
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='borrows'
                                , verbose_name='Библиотека')
    borrow_date = models.DateField(verbose_name='Дата выдачи')
    return_date = models.DateField(verbose_name='Срок возврата')
    returned = models.BooleanField(default=False, verbose_name='Книга возвращена')

    def is_overdue(self):
        """Проверить, что книга не возвращена, а срок возврата раньше текущей даты."""
        if self.returned:
            return False
        return self.return_date < timezone.now().date()

    def __str__(self):
        """Вернуть название книги и признак просрочки в виде Yes или No."""
        overdue = 'Yes' if self.is_overdue() else 'No'
        return f"Book '{self.book.title}' borrow period — Overdue?: {overdue}"


class Review(models.Model):
    """Отзыв участника о книге с обязательной оценкой от 1 до 5 и текстом."""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', verbose_name='Книга')
    reviewer = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='reviews'
                                 , verbose_name='Автор отзыва')
    rating = models.FloatField(verbose_name='Оценка'
                               , validators=[MinValueValidator(1.0
                                                               , message='Оценка должна быть не меньше 1.',)
        , MaxValueValidator(5.0, message='Оценка должна быть не больше 5.',)]
                               , help_text=('Введите число от 1 до 5 включительно, например 4.5. '
            'Если не хотите ставить оценку, оставьте поле пустым.'))
    description = models.TextField(verbose_name='Отзыв', blank=True,)

    def __str__(self):
        """Вернуть название книги и оценку из отзыва."""
        return  f"Book: {self.book.title}, Rating:{self.rating}"


class AuthorDetail(models.Model):
    """Дополнительные сведения об авторе со связью один-к-одному."""
    author = models.OneToOneField(Author, on_delete=models.CASCADE, related_name='details', verbose_name='Автор')
    biography = models.TextField(verbose_name='Биография')
    birth_city = models.CharField(max_length=50, verbose_name='Город рождения')
    gender = models.CharField(max_length=50, choices=Gender, verbose_name='Пол')

    def __str__(self):
        """Вернуть имя и фамилию связанного автора."""
        return f"{self.author.first_name} {self.author.last_name}"


class Event(models.Model):
    """Событие библиотеки с датой, временем и необязательным списком книг."""
    title = models.CharField(max_length=255,  verbose_name='Название события')
    description = models.TextField(verbose_name='Описание',)
    date = models.DateTimeField(verbose_name='Дата и время проведения',)
    library = models.ForeignKey(Library, verbose_name='Библиотека', on_delete=models.CASCADE, related_name='events')
    books = models.ManyToManyField(Book, verbose_name='Обсуждаемые книги', related_name='events', blank=True)

    def __str__(self):
        """Вернуть название события."""
        return self.title


class EventParticipant(models.Model):
    """Запись регистрации на событие с датой и связью с несколькими участниками."""
    event = models.ForeignKey(Event, verbose_name='Событие', on_delete=models.CASCADE, related_name='participants')
    member = models.ManyToManyField(Member, verbose_name='Участник', related_name='event_participations')
    registration_date = models.DateField(default=timezone.now, verbose_name='Дата регистрации')

    def __str__(self):
        """Вернуть строковое представление менеджера участников и название события."""
        return f'{self.member} — {self.event}'
