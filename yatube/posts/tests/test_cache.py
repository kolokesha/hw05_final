from .SetUp import SetUp
from ..models import Post
from django.urls import reverse

from django.core.cache import cache


class CacheTests(SetUp):

    def test_cache_correct(self):
        response = self.authorized_client.get(reverse('posts:index'))
        Post.objects.all().delete()
        self.assertEqual(response.content,
                         self.authorized_client.get(
                             reverse('posts:index')).content
                         )
        cache.clear()
        self.assertNotEqual(response.content,
                            self.authorized_client.get(
                                reverse('posts:index')).content
                            )
