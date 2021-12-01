from django.core.cache import cache
from django.urls import reverse

from ..models import Post
from .SetUp import SetUp


class CacheTests(SetUp):

    def test_cache_correct(self):
        response = self.client.get(reverse('posts:index'))
        post_1 = response.context['page_obj'][0]
        self.post.delete()
        post_2 = response.context['page_obj'][0]
        self.assertEqual(post_2, post_1)
        cache.clear()
        response = self.client.get(reverse('posts:index'))
        post_3 = response.context['page_obj'][0]
        self.assertNotEqual(post_3, post_1)
