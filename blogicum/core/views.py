"""View-функции для страниц ошшибок."""
from django.shortcuts import render


def page_not_found(request, exception):
    """Страница не найдена."""
    return render(request, 'pages/404.html', status=404)


def server_error(request, exception=None):
    """Ошибка сервера."""
    return render(request, 'pages/500.html', status=500)


def csrf_failure(request, reason=''):
    """Ошибка доступа."""
    return render(request, 'pages/403csrf.html', status=403)
