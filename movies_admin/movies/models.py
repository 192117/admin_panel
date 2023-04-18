from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from movies.mixins import TimeStampedMixin, UUIDMixin


class Genre(models.Model):

    name = models.CharField(_('name'), unique=True, max_length=255)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'content.genre'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Filmwork(TimeStampedMixin, UUIDMixin):

    class TypeFilm(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv_show', _('tv_show')

    title = models.TextField(_('title'), unique=True)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('created_date'))
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0), MaxValueValidator(100)])
    type_film = models.CharField(_('type_film'), max_length=7, choices=TypeFilm.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'content.film_work'
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'


class Person(TimeStampedMixin, UUIDMixin):

    full_name = models.TextField(_('full_name'), unique=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'content.person'
        verbose_name = 'Персона'
        verbose_name_plural = 'Персоны'


class GenreFilmwork(UUIDMixin):

    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content.genre_film_work'
        verbose_name = 'Жанр и кинопроизведение'
        verbose_name_plural = 'Жанры и кинопроизведения'

    def __str__(self):
        return f'{self.film_work}-{self.genre}'


class PersonFilmwork(UUIDMixin):

    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.TextField(_('role'), null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content.person_film_work'
        verbose_name = 'Персона и кинопроизведение'
        verbose_name_plural = 'Персоны и кинопроизведения'

    def __str__(self):
        return f'{self.film_work}-{self.person}'
