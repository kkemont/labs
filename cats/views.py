from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить кота", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contacts'},
        {'title': "Войти", 'url_name': 'login'}
        ]

descriptions = ["Большой Шлёпа (также известен как просто Шлёпа или Большой русский кот) — серия интернет-мемов с "
                "каракалом по кличке Гоша. В англоязычном сегменте Интернета распространено прозвище Floppa или "
                "Big Floppa.",
                "Бродячий кот по кличке Мистер Фреш прославился в соцсетях благодаря приложению Hello Street Cat, "
                "в котором можно давать донаты на корм. Привередливый кот, ждущий от поклонников только свежий корм в "
                "прямом эфире, стал героем мемов и фанартов."]

cats_db = [{'name': 'Большой Шлепа', 'weight': 20, 'id': 0, 'img': 'cats/images/bigfloppa.jpg', 'about': descriptions[0]},
           {'name': 'Мистер Фреш', 'weight': 6, 'id': 1, 'img': 'cats/images/mrfresh.png', 'about': descriptions[1]}]


navigation_db = [{'id': 0, 'name': 'Смешные'},
                 {'id': 1, 'name': 'Толстые'},
                 {'id': 2, 'name': 'Маленькие'}]


def index(request):
    data = {'title': 'Главная страница',
            'menu': menu,
            'cats': cats_db,
            'selected_id': 0
            }
    return render(request, 'cats/index.html', context=data)


def about(request):
    data = {'title': 'О сайте', 'menu': menu}
    return render(request, 'cats/about.html', data)


def show_concrete_cat(request, cat_id):
    return HttpResponse(f"<h2Статья о коте {cat_id}</h2>")


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
            'cats': cats_db,
            'selected_id': filter_id
            }
    return render(request, 'cats/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
