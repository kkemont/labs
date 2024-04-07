from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render, get_object_or_404
from cats.models import Cat


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить кота", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contacts'},
        {'title': "Войти", 'url_name': 'login'}
        ]

navigation_db = [{'id': 0, 'name': 'Смешные'},
                 {'id': 1, 'name': 'Толстые'},
                 {'id': 2, 'name': 'Маленькие'}]


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


def show_categories(request, filter_id):
    data = {'title': 'Главная страница',
            'menu': menu,
            'cats': Cat.published.all(),
            'selected_id': filter_id
            }
    return render(request, 'cats/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
