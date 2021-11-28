import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Post, Comment
from .SetUp import SetUp
from ..forms import PostForm

User = get_user_model()


class PostCreateFormTest(SetUp):

    # def tearDownClass(self):
    #     super().tearDownClass()
    #     shutil.rmtree(self.TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_post_create(self):
        post_count = Post.objects.count()
        """Проверка на создание поста в БД"""
        form_data = {
            'text': 'Testing form data'
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:profile',
                             kwargs={'username': self.user_author.username}))
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                author=self.user_author,
                text=form_data['text']
            ).exists()
        )

    def test_edit_post(self):
        """Тест редактирования"""
        form_data = {
            'text': 'Test edit'
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse('posts:post_detail',
                              kwargs={'post_id': self.post.pk}))
        self.assertTrue(
            Post.objects.filter(
                author=self.user_author,
                text=form_data['text']
            ).exists()
        )

    def test_comments(self):
        comments_count = Comment.objects.count()
        form_data = {
            'text': 'Текст комментария'
        }
        response = self.authorized_client.post(
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True
        )
        print(Comment.objects.get(pk=1).text)
        # self.assertEqual(Comment.objects.count(), comments_count + 1)
        self.assertTrue(
            Comment.objects.filter(
                post=self.post,
                text=form_data['text'],
                author=self.user_author
            ).exists()
        )

    def test_post_with_image(self):
        post_count = Post.objects.count()
        """Проверка на создание поста в БД c изображением"""
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'ну тест и что',
            'image': uploaded
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='ну тест и что',
                image='posts/small.gif'
            ).exists()
        )
