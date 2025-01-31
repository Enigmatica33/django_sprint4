"""Получаем список постов."""
from django.db.models import Count
from django.utils import timezone

from .models import Post


def posts_queryset(hide=False, annotate=False, model_manager=Post.objects):
    """Получаем список постов."""
    queryset = model_manager.select_related('author', 'location', 'category')
    if hide:
        queryset = queryset.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now())
    if annotate:
        queryset = queryset.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')
    return queryset
