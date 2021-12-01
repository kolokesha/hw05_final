from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User

COUNT_PER_PAGE = 10


def get_page_obj(request, model):
    if model._meta.verbose_name == 'Group':
        model_list = model.posts.all()
    else:
        model_list = model.objects.all()
    return get_page_obj_by_model_list(model_list, request)


def get_page_obj_by_model_list(model_list, request):
    paginator = Paginator(model_list, COUNT_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


@cache_page(20)
def index(request):
    page_obj = get_page_obj(request, Post)

    template = 'posts/index.html'
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    page_obj = get_page_obj(request, group)

    template = 'posts/group_posts.html'
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_list(request):
    groups = Group.objects.all()

    template = 'posts/group_list.html'
    context = {
        'groups': groups,
    }
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    page_obj = get_page_obj_by_model_list(post_list, request)
    count = post_list.count()

    if request.user.is_authenticated and Follow.objects.filter(
            user=request.user, author=author).exists():
        following = True
    else:
        following = False

    template = 'posts/profile.html'
    context = {
        'page_obj': page_obj,
        'posts_count': count,
        'author': author,
        'following': following,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()
    form = CommentForm(request.POST or None)
    template = 'posts/post_detail.html'
    context = {
        'post': post,
        'comments': comments,
        'form_comment': form
    }
    return render(request, template, context)


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user)

    template = 'posts/create_post.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    author = request.user
    post = get_object_or_404(Post, pk=post_id)
    if author != post.author:
        return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post)
    if form.is_valid():
        post.save()
        return redirect('posts:post_detail', post_id=post_id)

    template = 'posts/create_post.html'
    context = {
        'form': form,
        'post': post,
    }
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    follower_posts = Post.objects.filter(author__following__user=request.user)
    page_obj = get_page_obj_by_model_list(follower_posts, request)
    context = {
        'page_obj': page_obj,
        'posts': follower_posts,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.add_follow(request.user, author)
    return redirect('posts:profile', username=author.username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.del_follow(request.user, author)
    return redirect('posts:profile', username=author.username)
