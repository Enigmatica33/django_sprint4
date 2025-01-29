"""Формы."""
from django import forms

from .models import Post, Comment, User


class PostForm(forms.ModelForm):
    """Форма создания, редактирования, удаления постов."""

    class Meta:
        """Класс Мета."""

        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M')
        }


class CommentForm(forms.ModelForm):
    """Форма создания, редактирования, удаления комментариев."""

    class Meta:
        """Класс Мета."""

        model = Comment
        fields = ('text',)


class UserForm(forms.ModelForm):
    """Форма редактирования профиля пользователя."""

    class Meta:
        """Класс Мета."""

        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
