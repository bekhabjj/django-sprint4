from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from blog.constants import MAX_LENGTH, MAX_WORDS_LENGTH

User = get_user_model()


class PublishedBaseModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Добавлено",
    )

    class Meta:
        abstract = True


class Category(PublishedBaseModel):
    title = models.CharField(
        max_length=MAX_LENGTH,
        unique=True,
        verbose_name="Заголовок",
    )
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(
        unique=True,
        verbose_name="Идентификатор",
        help_text=(
            "Идентификатор страницы для URL; разрешены "
            "символы латиницы, цифры, дефис и подчёркивание."
        ),
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"
        ordering = ("title",)

    def __str__(self):
        return self.title[:MAX_WORDS_LENGTH]


class Location(PublishedBaseModel):
    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="Название места",
    )

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"
        ordering = ("name",)

    def __str__(self):
        return self.name[:MAX_WORDS_LENGTH]


class Post(PublishedBaseModel):
    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="Заголовок",
    )
    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем — можно делать "
            "отложенные публикации."
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
    )
    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="posts_images",
        blank=True,
    )

    class Meta:
        default_related_name = "posts"
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.title[:MAX_WORDS_LENGTH]

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.pk])


class Comment(PublishedBaseModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="Пост",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    text = models.TextField("Текст комментария")

    class Meta:
        default_related_name = "comments"
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("created_at",)

    def __str__(self):
        return f'Комментарий {self.text[:MAX_WORDS_LENGTH]} от {self.author}'
