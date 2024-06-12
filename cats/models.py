from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Cat.Status.PUBLISHED)


class Cat(models.Model):
    class Meta:
        ordering = ['-time_create']
        indexes = [models.Index(fields=['-time_create'])]
        verbose_name = 'Коты'
        verbose_name_plural = 'Коты'

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    objects = models.Manager()
    published = PublishedModel()

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Содержимое')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default=Status.DRAFT, verbose_name='Статус')
    img = models.CharField(max_length=255, blank=True, verbose_name='Адрес изображения')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name='Фото')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категории')
    tags = models.ManyToManyField('TagPosts', blank=True, related_name='tags', verbose_name='Тэги')
    owners = models.OneToOneField('Owners', on_delete=models.SET_NULL, null=True, blank=True, related_name='pet', verbose_name='Владельцы')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True, default=None)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})


class TagPosts(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Owners(models.Model):
    name = models.CharField(max_length=100)
    count = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')


class Comment(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='comments', null=True,
                               default=None)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    content = models.TextField(blank=True, verbose_name='Комментарий')
    post = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.content


class Like(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='likes', null=True,
                               default=None)
    post = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='likes')


class Dislike(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='dislikes', null=True,
                               default=None)
    post = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='dislikes')
