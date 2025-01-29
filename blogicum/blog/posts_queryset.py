"""Получаем список постов."""
from django.db.models import Q
from django.utils import timezone

from .models import Post


# def posts_queryset(model_manager=Post.objects, ):
#     """Получаем список постов."""
#     return model_manager.filter(
#         Q(is_published=True) | Q(author_id=request.user.id),
#         Q(category__is_published=True) | Q(author_id=request.user.id),
#         Q(pub_date__lte=timezone.now()) | Q(author_id=request.user.id)
#     ).select_related('author', 'location', 'category')

def posts_queryset(model_manager=Post.objects, published = True, postponed = False):
    """Получаем список постов."""
    queryset = model_manager.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).select_related('author', 'location', 'category')
    if 