from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from movies.models import Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Filmwork.objects.annotate(
            genres=ArrayAgg('genres_list__name', distinct=True),
            actors=ArrayAgg('personfilmwork__person__full_name',
                            filter=Q(personfilmwork__role='actor'),
                            distinct=True),
            directors=ArrayAgg('personfilmwork__person__full_name',
                               filter=Q(personfilmwork__role='director'),
                               distinct=True),
            writers=ArrayAgg('personfilmwork__person__full_name',
                             filter=Q(personfilmwork__role='writer'),
                             distinct=True),
        ).values(
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type',
            'genres',
            'actors',
            'directors',
            'writers',
        ).order_by('created')
        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)
