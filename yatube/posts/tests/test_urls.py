from http import HTTPStatus

from django.contrib.auth import get_user_model

from .SetUp import SetUp
from ..models import Follow

User = get_user_model()


class PostURLTests(SetUp):

    def test_post_urls_uses_correct_template(self):
        templates_urls_names = {
            '/': 'posts/index.html',
            '/group/': 'posts/group_list.html',
            f'/group/{self.group.slug}/': 'posts/group_posts.html',
            f'/profile/{self.user_author.username}/': 'posts/profile.html',
            f'/posts/{self.post.pk}/': 'posts/post_detail.html',
            f'/posts/{self.post.pk}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }
        for address, template in templates_urls_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_post_urls_uses_correct_template_for_guest(self):
        templates_urls_names = {
            '/': 'posts/index.html',
            '/group/': 'posts/group_list.html',
            f'/group/{self.group.slug}/': 'posts/group_posts.html',
            f'/profile/{self.user_author.username}/': 'posts/profile.html',
            f'/posts/{self.post.pk}/': 'posts/post_detail.html',
        }
        for address, template in templates_urls_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_post_id_access_author(self):
        """ /posts/id.post/edit и create доступ автору и авторизованному"""
        templates_urls_names = [
            f'/posts/{self.post.pk}/edit/',
            '/create/'
        ]
        for url in templates_urls_names:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_redirect(self):
        """Страница по адресу /posts/post.id/edit перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get(f'/posts/{self.post.pk}/edit/',
                                         follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/posts/2/edit/'
        )

    def test_post_create_redirect(self):
        """Страница по адресу /create/ перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/create/')

    def test_post_create_comment_redirect(self):
        """Страница по адресу post/1/comment перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get(f'/posts/{self.post.pk}/comment',
                                         follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/posts/2/comment')
