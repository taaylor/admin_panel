from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.models import Filmwork


class MoviesApiMixin:
    http_method_names = ["get"]

    def get_queryset(self):
        films = Filmwork.objects.annotate(
            genre=ArrayAgg("genres__name", distinct=True),
            actor=ArrayAgg(
                "persons__full_name",
                filter=Q(personfilmwork__role="actor"),
                distinct=True,
            ),
            directors=ArrayAgg(
                "persons__full_name",
                filter=Q(personfilmwork__role="directors"),
                distinct=True,
            ),
            writers=ArrayAgg(
                "persons__full_name",
                filter=Q(personfilmwork__role="writers"),
                distinct=True,
            ),
        ).values(
            "id",
            "title",
            "description",
            "creation_date",
            "rating",
            "type",
            "genre",
            "actor",
            "directors",
            "writers",
        )
        return films

    def render_to_response(self, context, **respons_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, self.paginate_by
        )
        context = {
            "count": paginator.count,
            "total_pages": page.paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            "results": list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return self.object
