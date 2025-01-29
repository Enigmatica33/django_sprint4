"""Получаем список постов."""
from django.db.models import Count
from django.utils import timezone

from .models import Post


def posts_queryset(author=None, comments=None, model_manager=Post.objects):
    """Получаем список постов."""
    queryset = model_manager.all()
    if comments is True:
        queryset = queryset.select_related('author')
        return queryset
    if author is None:
        queryset = queryset.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()).select_related(
                'author',
                'location',
                'category').annotate(
                    comment_count=Count('comments')
        ).order_by('-pub_date')
    else:
        queryset = queryset.filter(author_id=author).select_related(
            'author',
            'location',
            'category').annotate(
                comment_count=Count('comments')
        ).order_by('-pub_date')
    return queryset
