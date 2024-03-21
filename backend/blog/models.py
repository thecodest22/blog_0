from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex
from django.core.validators import FileExtensionValidator
from django.db.models.functions import Now, Upper

from treebeard.mp_tree import MP_Node


class Post(models.Model):
    """
    Модель поста в блоге.
    """

    class PostStatusChoices(models.TextChoices):
        PUBLISHED = 'PUBLISHED', 'Опубликовано'
        DRAFT = 'DRAFT', 'Черновик'

    title = models.CharField(
        verbose_name='Заголовок',
        max_length=255
    )
    slug = models.SlugField(
        verbose_name='Представление в URL',
        max_length=255,
        unique=True
    )
    annotation = models.CharField(
        verbose_name='Краткое описание',
        max_length=255,
        blank=True,
        null=True
    )
    content = models.TextField(
        verbose_name='Содержимое поста',
    )
    picture = models.ImageField(
        verbose_name='Изображение',
        upload_to='posts/',
        validators=(
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'gif']
            ),
        ),
        blank=True
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=10,
        choices=PostStatusChoices,
        default=PostStatusChoices.DRAFT
    )
    created_at = models.DateTimeField(
        verbose_name='Опубликован',
        auto_now_add=True,
        db_default=Now(),
    )
    updated_at = models.DateTimeField(
        verbose_name='Обновлен',
        auto_now=True,
        db_default=Now(),
    )
    is_fixed = models.BooleanField(
        verbose_name='Зафиксирован',
        default=False
    )
    author = models.ForeignKey(
        verbose_name='Автор',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='created_posts'
    )
    updater = models.ForeignKey(
        verbose_name='Обновил',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='updated_posts',
        blank=True,
        null=True
    )
    section = models.ForeignKey(
        verbose_name='Раздел',
        to='blog.Section',
        on_delete=models.PROTECT,
        related_name='posts'
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-created_at',)
        indexes = (
            BrinIndex(fields=('created_at',)),
            models.Index(Upper('title'), name='post_title_upper'),
            models.Index(Upper('slug'), name='post_slug_upper')
        )

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        print(1)
        super().save(**kwargs)


class Section(MP_Node):
    """
    Раздел постов.
    """

    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    slug = models.SlugField(
        verbose_name='Представление в URL',
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=300
    )

    node_order_by = ('title',)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        indexes = (
            models.Index(Upper('title'), name='section_title_upper'),
            models.Index(Upper('slug'), name='section_slug_upper')
        )

    def __str__(self):
        return self.title
