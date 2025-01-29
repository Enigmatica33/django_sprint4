"""Модели."""
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

MAX_TITLE_LENGTH = 256


class PublishedModel(models.Model):
    """Модель PublishedModel."""

    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Добавлено"
    )

    class Meta:
        """Внутренний класс Meta модели."""

        abstract = True


class Location(PublishedModel):
    """Модель Location."""

    name = models.CharField(
        max_length=MAX_TITLE_LENGTH,
        verbose_name="Название места")

    class Meta:
        """Внутренний класс Meta модели."""

        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        """Магический метод."""
        return self.name[:MAX_TITLE_LENGTH]


class Category(PublishedModel):
    """Модель Category."""

    title = models.CharField(
        max_length=MAX_TITLE_LENGTH,
        verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(
        unique=True,
        verbose_name="Идентификатор",
        help_text=(
            "Идентификатор страницы для URL; "
            "разрешены символы латиницы, цифры, дефис и подчёркивание."
        ),
    )

    class Meta:
        """Внутренний класс Meta модели."""

        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        """Магический метод."""
        return self.title[:MAX_TITLE_LENGTH]


class Post(PublishedModel):
    """Модель Post."""

    title = models.CharField(
        max_length=MAX_TITLE_LENGTH,
        verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем "
            "— можно делать отложенные публикации."
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
    )
    location = models.ForeignKey(
        Location,
        blank=True,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
    )
    image = models.ImageField(
        verbose_name='Фото',
        upload_to='posts_images',
        blank=True)

    class Meta:
        """Внутренний класс Meta модели."""

        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        default_related_name = "posts"
        ordering = ('-pub_date',)

    def __str__(self):
        """Магический метод."""
        return self.title[:MAX_TITLE_LENGTH]

    @property
    def comment_count(self):
        """Подсчет количества комменатриев отдельного поста."""
        return self.comments.count()


class Comment(PublishedModel):
    """Модель Comment."""

    text = models.TextField(
        verbose_name='Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    class Meta:
        """Внутренний класс Meta модели."""

        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ('created_at',)

    def __str__(self):
        """Магический метод."""
        return str(self.text)[:10]
