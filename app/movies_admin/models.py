from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from model_utils.models import TimeStampedModel
import uuid


class Genre(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        _('название'),
        max_length=255,
        db_index=True,
    )
    description = models.TextField(_('описнаие'), blank=True)

    class Meta:
        verbose_name = _('жанр')
        verbose_name_plural = _('жанры')

    def __str__(self):
        return self.name


class FilmworkType(models.TextChoices):

    MOVIE = 'movie', _('фильм')
    TV_SHOV = 'tv_show', _('шоу')


class MPAARating(models.TextChoices):

    G = 'G', _('без ограничений')
    PG = 'PG', _('детям рекомендуется смотреть фильм с родителями')
    PG_13 = 'PG-13', _('просмотр не желателен детям до 13 лет')
    R = 'R', _('лица, не достигшие 17-летнего возраста, только в сопровождении родителей')
    NC_17 = 'NC-17', _('лица 17-летнего возраста и младше не допускаются')


class RoleType(models.TextChoices):

    ACTOR = 'actor', _('актер')
    WRITER = 'writer', _('сценарист')
    DIRECTOR = 'director', _('рижесер')


class Person(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('имя'), max_length=255)
    surname = models.CharField(_('фамилия'), max_length=255, default='')

    class Meta:
        verbose_name = _('человек')
        verbose_name_plural = _('люди')

    def __str__(self):
        return f'{self.surname} {self.name}'


class Filmwork(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('назание'), max_length=255)
    description = models.TextField(_('описание'), blank=True)
    creation_date = models.DateField(_('дата создания фильма'), blank=True, db_index=True, null=True)
    pg_raiting = models.CharField(
        _('тип'),
        max_length=20,
        choices=MPAARating.choices,
        default=None,
        null=True,
    )

    file_path = models.FileField(_('файл'), upload_to='film_works/', blank=True)
    rating = models.FloatField(
        _('рейтинг'),
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ],
        blank=True,
        db_index=True,
    )
    type = models.CharField(_('тип'), max_length=20, choices=FilmworkType.choices, default=None)

    genres = models.ManyToManyField(
        Genre,
        through='MoviesGenres',
    )

    persons = models.ManyToManyField(
        Person,
        related_name='in_films',
        related_query_name='film',
        blank=True,
        through='MoviesPersons',
    )

    class Meta:
        verbose_name = _('кинопроизведение')
        verbose_name_plural = _('кинопроизведения')

    def __str__(self):
        return self.title


class MoviesPersons(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filmwork = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(_('тип занятости'), max_length=20, choices=RoleType.choices)

    class Meta:
        unique_together = ['filmwork', 'person', 'role']

    def __str__(self):
        return f'{self.person.surname} {self.person.name}'
    

class MoviesGenres(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filmwork = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['filmwork', 'genre']

    def __str__(self):
        return f'{self.genre.name}'
