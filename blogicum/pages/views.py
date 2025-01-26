"""Представления для статичных страниц."""
from django.shortcuts import render
from django.views.generic import TemplateView


class About(TemplateView):
    """Отображение статичной страницы О проекте."""

    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        """Получение словаря контекста из родительского метода."""
        context = super().get_context_data(**kwargs)
        return context


class Rules(TemplateView):
    """Отображение статичной страницы Правила."""

    template_name = 'pages/rules.html'

    def get_context_data(self, **kwargs):
        """Получение словаря контекста из родительского метода."""
        context = super().get_context_data(**kwargs)
        return context


def page_not_found(request, exception):
    """Страница не найдена."""
    return render(request, 'pages/404.html', status=404)


def server_error(request, exception=None):
    """Ошибка сервера."""
    return render(request, 'pages/500.html', status=500)


def csrf_failure(request, reason=''):
    """Ошибка доступа."""
    return render(request, 'pages/403csrf.html', status=403)
