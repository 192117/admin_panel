from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from .mixins import MoviesApiMixin


class MoviesListApi(MoviesApiMixin, BaseListView):

    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):

        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by,
        )
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):

        context = self.object

        return context
