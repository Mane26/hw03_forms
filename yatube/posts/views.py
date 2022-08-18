from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User

# Используем переменную константу COUNT_LAST_POSTS,
# требуется вывести последние 10 постов


def group_posts(request, group_name):
    # Страница со списком постов - group_posts,
    # отвечающая за запросы, содержимое постов из групп
    groups = get_object_or_404(Group, slug=group_name)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(page_number)
    context = {
        'group': groups,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author)
    # posts = author.author.select_related('group', 'author')
    page_obj = Paginator(posts, request)
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    '''Страница для просмотра одного поста'''
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post, }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author)
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    form = PostForm(None, instance=post)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    if request.method == 'Post':
        form = PostForm(request.Post, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id=post_id)
        return render(request, 'posts/create_post.html',
                      {'form': form, 'is_edit': True})
    return render(request, 'posts/create_post.html',
                  {'form': form, 'is_edit': True})


def authorized_only(func):
    def check_user(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Возвращает view-функцию, если пользователь авторизован.
            return func(request, *args, **kwargs)
        # Если пользователь не авторизован — отправим его на страницу логина.
        return redirect('/auth/login/')
    return check_user
