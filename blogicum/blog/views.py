"""Представления."""
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView

from .forms import PostForm, CommentForm, UserForm
from .models import Post, Category, User, Comment


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
                'category')
    else:
        queryset = queryset.filter(author_id=author).select_related(
            'author',
            'location',
            'category')
    return queryset


def index(request):
    """Главная страница."""
    post_list = posts_queryset()
    context = page_paginator(post_list, request)
    return render(request, 'blog/index.html', context)


def page_paginator(queryset, request):
    """Пагинатор."""
    paginator = Paginator(queryset, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {'page_obj': page_obj}


def post_detail(request, post_id):
    """Страница отдельного поста."""
    instance = get_object_or_404(Post, id=post_id)
    if instance.author == request.user:
        post = get_object_or_404(
            posts_queryset(author=request.user),
            id=post_id)
    else:
        post = get_object_or_404(posts_queryset(), id=post_id)
    form = CommentForm(request.POST or None)
    # comments = post.comments.select_related('author') # работает
    comments = posts_queryset(model_manager=post.comments, comments=True)
    return render(
        request, 'blog/detail.html',
        {'post': post, 'comments': comments, 'form': form}
    )


def category_posts(request, category_slug):
    """Страница с постами в выбранной категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = posts_queryset(model_manager=category.posts)
    context = {'category': category}
    context.update(page_paginator(post_list, request))
    return render(
        request, 'blog/category.html',
        context
    )


def profile(request, username):
    """Страница пользователя."""
    profile = get_object_or_404(User, username=username)
    context = {'profile': profile}
    if request.user.username == username:
        post = posts_queryset(author=request.user.id)
    else:
        post = posts_queryset()
    context.update(page_paginator(post, request))
    return render(
        request,
        'blog/profile.html',
        context
    )


def edit_profile(request):
    """Редактирование профиля пользователя."""
    instance = get_object_or_404(User, username=request.user.username)
    form = UserForm(
        request.POST or None,
        files=request.FILES or None,
        instance=instance
    )
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect('blog:profile', request.user.username)
    return render(
        request,
        'blog/user.html',
        context
    )


@login_required
def create_post(request):
    """Создание нового поста пользователя."""
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )
    context = {'form': form}
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        return redirect('blog:profile', request.user.username)
    return render(request, 'blog/create.html', context)


# @login_required
def edit_post(request, post_id):
    """Редактирование поста пользователя."""
    instance = get_object_or_404(Post, id=post_id)
    if (request.user != instance.author):
        return redirect('blog:post_detail', post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=instance
    )
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(
        request,
        'blog/create.html',
        context
    )


@login_required
def delete_post(request, post_id):
    """Удаление поста пользователя."""
    instance = get_object_or_404(Post, id=post_id)
    if (request.user != instance.author and not request.user.is_superuser):
        return redirect('blog:post_detail', post_id=post_id)
    form = PostForm(request.POST or None, instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:profile', request.user.username)
    return render(request, 'blog/create.html', context)


@login_required
def add_comment(request, post_id):
    """Добавление комментария."""
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    """Редактирование комментария."""
    instance = get_object_or_404(Comment, id=comment_id)
    if (request.user != instance.author):
        return redirect('blog:post_detail', post_id=post_id)
    form = CommentForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/create.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    """Удаление комментария."""
    instance = get_object_or_404(Comment, id=comment_id)
    if (request.user != instance.author and not request.user.is_superuser):
        return redirect('blog:post_detail', post_id=post_id)
    context = {'instance': instance}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', context)


# class RegistrationCreateView(CreateView):
#     template_name = 'registration/registration_form.html',
#     form_class = UserCreationForm,
#     success_url = reverse_lazy('blog:index')
