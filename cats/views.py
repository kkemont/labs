from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from cats.models import Cat, Category, TagPosts


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить кота", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contacts'},
        {'title': "Войти", 'url_name': 'login'}
        ]


def index(request):
    cats = Cat.published.all()
    data = {'title': 'Главная страница',
            'menu': menu,
            'cats': cats,
            'selected_id': 0
            }
    return render(request, 'cats/index.html', context=data)


def about(request):
    data = {'title': 'О сайте', 'menu': menu}
    return render(request, 'cats/about.html', data)


def show_concrete_cat(request, post_slug):
    post = get_object_or_404(Cat, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'selected_id': 1
    }
    return render(request, 'cats/post.html', context=data)


def login(request):
    data = {'title': 'О сайте', 'menu': menu}
    return render(request, 'cats/login.html', data)


def contacts(request):
    data = {'title': 'О сайте', 'menu': menu}
    return render(request, 'cats/contacts.html', data)


def add_page(request):
    data = {'title': 'О сайте', 'menu': menu}
    return render(request, 'cats/addpage.html', data)


def show_categories(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Cat.published.filter(category_id=category.pk)
    data = {'title': f'Рубрика: {category.name}',
            'menu': menu,
            'cats': posts,
            'selected_id': category.pk
            }
    return render(request, 'cats/index.html', context=data)


def show_tag_posts(request, tag_slug):
    tag = get_object_or_404(TagPosts, slug=tag_slug)
    posts = tag.tags.filter(is_published=Cat.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'cats': posts,
        'cat_selected': None
    }
    return render(request, 'cats/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
