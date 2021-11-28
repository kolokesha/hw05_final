import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.conf import settings
from django.core.cache import cache

from ..models import Group, Post, Comment,Follow
from ..forms import PostForm, CommentForm

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


class SetUp(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.group_another = Group.objects.create(
            title='Тестовая группа 2',
            slug='test-slug-another',
            description='Тестовое описание 2',
        )
        cls.user_author = User.objects.create_user(username='HasNoName')
        cls.user_follower = User.objects.create_user(username='Follower')
        cls.post_author = Post.objects.create(
            author=cls.user_follower,
            text='ещё одинтест'
        )
        cls.post = Post.objects.create(
            author=cls.user_author,
            text='ну тест и что',
            group=cls.group
        )

        cls.comment = Comment.objects.create(
            author=cls.user_author,
            post=cls.post,
            text='Текст комментария'
        )
        cls.follow = Follow.objects.create(
            user=cls.user_follower,
            author=cls.user_author,
        )
        cls.form = PostForm()
        cls.form_comment = CommentForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_author)
        self.follower = Client()
        self.follower.force_login(self.user_follower)
        cache.clear()