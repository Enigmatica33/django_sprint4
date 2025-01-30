from django.core.paginator import Paginator
from django.conf import settings


def page_paginator(queryset, request):
    """Пагинатор."""
    paginator = Paginator(queryset, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {'page_obj': page_obj}
