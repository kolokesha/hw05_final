from django import forms
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import Follow, Group, Post
from ..views import COUNT_PER_PAGE
from .SetUp import SetUp

User = get_user_model()


class PostsPagesTests(SetUp):

    def test_post_urls_uses_correct_template(self):
        templates_urls_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_lists'): 'posts/group_list.html',
            reverse('posts:group_posts',
                    kwargs={
                        'slug': self.group.slug}): 'posts/group_posts.html',
            reverse('posts:profile', kwargs={
                'username': self.user_author.username}): 'posts/profile.html',
            reverse('posts:post_detail',
                    kwargs={
                        'post_id': self.post.pk}): 'posts/post_detail.html',
            reverse('posts:post_edit',
                    kwargs={
                        'post_id': self.post.pk}): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        for url, template in templates_urls_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_paginator_posts(self):
        """Шаблоны с пагинатором"""
        urls = [
            reverse('posts:index'),
            reverse('posts:group_posts', kwargs={'slug': self.group.slug}),
            reverse('posts:profile',
                    kwargs={'username': self.user_author.username})
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                first_object = response.context['page_obj'][0]
                post_text_0 = first_object.text
                self.assertEqual(post_text_0, self.post.text)

    def test_post_detail_edit_correct(self):
        """Проверка post_detail и post_edit на context и форму"""
        urls = [
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk}),
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}),
        ]
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        response = self.authorized_client.get(reverse(
            'posts:post_edit',
            kwargs={'post_id': self.post.pk}
        )
        )
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                first_object = response.context['post'].text
                self.assertEqual(first_object, self.post.text)

    def test_post_create_correct(self):
        """Проверка post_create на context"""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_is_not_in_other_group(self):
        """ Проверка на не вхождение поста в другую группу"""
        response = self.authorized_client.get(reverse(
            'posts:group_posts', kwargs={'slug': self.group_another.slug}))
        group_another_post = response.context['page_obj']
        self.assertNotIn(self.post,
                         group_another_post)


class PaginatorViewsTest(SetUp):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for post in range(1, 13):
            Post.objects.create(
                author=cls.user_author,
                text=f'Тест поста {post}',
                group=Group.objects.get(slug='test-slug')
            )

    def test_index_contains_ten_records(self):
        """Тест paginator"""
        urls = [
            reverse('posts:index'),
            reverse('posts:group_posts', kwargs={'slug': self.group.slug}),
            reverse("posts:profile",
                    kwargs={'username': self.user_author.username})
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(len(response.context['page_obj']),
                                 COUNT_PER_PAGE)
                response = self.client.get(url + '?page=2')
                if url == reverse('posts:index'):
                    self.assertEqual(len(response.context['page_obj']), 4)
                else:
                    self.assertEqual(len(response.context['page_obj']), 3)


class FollowViewsTests(SetUp):

    def test_follow_create(self):
        """Проверка подписки на автора авторизованным пользователем
        """
        self.assertFalse(Follow.objects.filter(
            user=self.user_author, author=self.user_follower).exists())
        response = self.authorized_client.get(reverse(
            'posts:profile_follow', kwargs={'username': self.user_follower})
        )
        self.assertRedirects(
            response,
            reverse('posts:profile',
                    kwargs={'username': self.user_follower}))
        self.assertTrue(Follow.objects.filter(
            user=self.user_author, author=self.user_follower).exists())

    def test_unfollow(self):
        """Тест отписки от автора """

        self.authorized_client.get(reverse(
            'posts:profile_follow', kwargs={'username': self.user_follower})
        )
        self.assertTrue(Follow.objects.filter(
            user=self.user_author, author=self.user_follower).exists())
        response = self.authorized_client.get(reverse(
            'posts:profile_unfollow',
            kwargs={'username': self.user_follower}))
        self.assertRedirects(
            response,
            reverse('posts:profile',
                    kwargs={'username': self.user_follower}))
        self.assertFalse(Follow.objects.filter(
            user=self.user_author, author=self.user_follower).exists())

    def test_follow_index(self):
        """ Тест списка постов follow"""
        self.authorized_client.get(reverse(
            'posts:profile_follow', kwargs={'username': self.user_follower}))
        response_follower = self.authorized_client.get(
            reverse('posts:follow_index'))
        response_not_follower = self.follower.get(
            reverse('posts:follow_index'))
        self.assertEqual(
            response_follower.context['posts'][0].text, self.post_author.text)
        self.assertNotEqual(response_not_follower.context['posts'][0].text,
                            self.post_author.text)

