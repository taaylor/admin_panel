from django.contrib import admin
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


class GenresFilter(admin.SimpleListFilter):
    title = _("genre")
    parameter_name = "genre"

    def lookups(self, request, model_admin) -> list[str]:
        genres = Genre.objects.all().distinct().values_list("id", "name")
        return genres

    def queryset(self, request, queryset) -> QuerySet[Genre]:
        if self.value():
            return queryset.filter(genres__id=self.value()).distinct()
        return queryset


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "modified")
    search_fields = ("name", "description")
    ordering = ("name",)


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = (
        "title",
        "type",
        "creation_date",
        "rating",
    )
    list_filter = ("type", GenresFilter)
    ordering = ("title", "rating")
    search_fields = ("title", "description", "id")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    # inlines = (PersonFilmworkInline,)
    ordering = ("full_name",)
    list_display = ("full_name", "modified")
    search_fields = ("full_name",)
