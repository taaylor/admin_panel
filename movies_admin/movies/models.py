import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_("modified"), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("full_name"), max_length=255)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("Actor")
        verbose_name_plural = _("Actors")

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):

    class FilmworkType(models.TextChoices):
        MOVIE = "movie", _("movie")
        TV_SHOW = "tv_show", _("tv_show")
        SERIAL = "serial", _("serial")

    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    creation_date = models.DateField(_("creation_date"), null=True)
    rating = models.DecimalField(
        _("rating"),
        default=0.0,
        decimal_places=1,
        max_digits=3,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    type = models.CharField(_("type"), choices=FilmworkType.choices)
    certificate = models.CharField(_("certificate"), max_length=512, blank=True)
    file_path = models.FileField(_("file"), blank=True, null=True, upload_to="movies/")
    genres = models.ManyToManyField(
        to=Genre, through="GenreFilmwork", verbose_name=_("genres")
    )
    persons = models.ManyToManyField(
        to=Person, through="PersonFilmwork", verbose_name=_("persons")
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("Film")
        verbose_name_plural = _("Films")
        indexes = [
            models.Index(
                fields=["creation_date", "rating"],
                name="filmwork_createdate_rating_idx",
            ),
            models.Index(fields=["rating"], name="film_work_rating_idx"),
        ]


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        to="Filmwork", on_delete=models.CASCADE, verbose_name=_("film_work")
    )
    genre = models.ForeignKey(
        to="Genre", on_delete=models.CASCADE, verbose_name=_("genre")
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'

        constraints = [
            models.UniqueConstraint(
                fields=["film_work_id", "genre_id"],
                name="film_work_genre_idx",
            )
        ]


class RoleType(models.TextChoices):
    ACTOR = "actor", _("actor")
    DIRECTOR = "director", _("director")
    WRITER = "writer", _("writer")


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        to="Filmwork", on_delete=models.CASCADE, verbose_name=_("film_work")
    )
    person = models.ForeignKey(
        to="Person", on_delete=models.CASCADE, verbose_name=_("person")
    )
    role = models.TextField(_("role"), null=True, choices=RoleType.choices)
    created = models.DateTimeField(_("created"), auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'

        constraints = [
            models.UniqueConstraint(
                fields=["film_work_id", "person_id", "role"],
                name="film_work_person_idx",
            ),
        ]
