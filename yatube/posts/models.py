from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Group'


class Post(models.Model):
    text = models.TextField(
        'Текст поста',
        help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='Группа',
        help_text='Выберите группу'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    def __str__(self):
        return f'{self.text[:15]}'

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Post'


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата комментария',
        auto_now_add=True
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name="Подписывающийся юзер",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    @staticmethod
    def add_follow(follower, following):
        new_follow = Follow(user=follower, author=following)
        new_follow.save()

    @staticmethod
    def del_follow(follower, following):
        del_follow = get_object_or_404(Follow, user=follower, author=following)
        del_follow.delete()

