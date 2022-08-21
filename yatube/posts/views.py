from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User

POSTS_NUMB = 10


def group_posts(request, slug):
    # Функция group_posts передает данные в шаблон group_list.html
    group = get_object_or_404(Group, slug=slug)
    post_list = (group.posts.select_related("author").
                 order_by('-pub_date'))
    paginator = Paginator(post_list, POSTS_NUMB)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def index(request):
    # Функция index передает данные в шаблон index.html
    # Паджинация 10 постов на страницу
    post_list = (Post.objects.select_related("author").
                 order_by('-pub_date'))
    paginator = Paginator(post_list, POSTS_NUMB)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Здесь код запроса к модели и создание словаря контекста
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    author = get_object_or_404(User, username=username)
    # В тело страницы выведен список постов
    post_list = (author.posts.select_related("author").
                 order_by('-pub_date'))
    # Выведено общее количество постов пользователя
    count = author.posts.count()
    # Паджинация 10 постов на страницу
    paginator = Paginator(post_list, POSTS_NUMB)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'count': count,
        'posts': post_list,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
    post = get_object_or_404(Post, pk=post_id)
    # В тело страницы выведен один пост, выбранный по pk
    context = {'post': post, }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    # Добавлена "Новая запись" для авторизованных пользователей
    if request.method == "POST":
        form = PostForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author.username)
        return render(request, 'posts/post_create.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/post_create.html', {'form': form})


@login_required
def post_edit(request, post_id):
    # Добавлена страница редактирования записи
    # Права на редактирование должны быть только у автора этого поста
    # Остальные пользователи должны перенаправляться
    # На страницу просмотра поста
    post = Post.objects.get(pk=post_id)
    form = PostForm(None, instance=post)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    return render(
        request,
        'posts/post_create.html',
        {'form': form, 'is_edit': True, 'post_id': post_id})
