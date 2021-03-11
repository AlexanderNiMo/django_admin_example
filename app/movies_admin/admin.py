from django.contrib import admin
from .models import Filmwork, Person, Genre
from django.utils.translation import gettext_lazy as _


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


class PersonRoleInline(admin.TabularInline):
    model = Filmwork.persons.through
    extra = 0
    verbose_name = _('участник')
    verbose_name_plural = _('участники')


class GenreInline(admin.TabularInline):
    model = Filmwork.genres.through
    extra = 0
    verbose_name = _('жанр')
    verbose_name_plural = _('жанры')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):

    search_fields = ('title', 'description', 'id')

    list_filter = ('type',)

    list_display = ('title', 'type', 'creation_date', 'rating')

    fields = (
        'title', 'type', 'description', 'creation_date', 'pg_raiting',
        'file_path', 'rating'
    )

    inlines = [
        PersonRoleInline,
        GenreInline
    ]