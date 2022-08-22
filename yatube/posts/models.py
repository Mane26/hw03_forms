from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """ Создание модели для таблицы Сообщества."""
    title = models.CharField(max_length=200, verbose_name='Group title')
    slug = models.SlugField(unique=True, verbose_name='Relative URL')
    description = models.TextField(
        null=True, blank=True,
        verbose_name='Group description'
    )

    def _str_(self) -> str:
        return self.title


class Post(models.Model):
    """ Создание модели для таблицы Постов."""
    text = models.TextField(
        max_length=300, verbose_name="текст поста")
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts'
    )
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    class Meta:
        verbose_name = 'Пост'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text
