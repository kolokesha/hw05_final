from django.core.cache import cache
from django.urls import reverse

from ..models import Post
from .SetUp import SetUp


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
