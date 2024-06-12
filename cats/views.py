from django.http import HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from cats.models import Cat, TagPosts, UploadFiles, Like, Dislike
from cats.forms import UploadFileForm, AddCommentForm
from cats.utils import DataMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить кота", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contacts'},
        {'title': "Войти", 'url_name': 'login'}
        ]


class CatsHome(DataMixin, ListView):
    template_name = 'cats/index.html'
    context_object_name = 'cats'

    def get_queryset(self):
        return Cat.published.all().select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_mixin_context(
            super().get_context_data(**kwargs),
            title='Главная страница',
            selected_id=0
        )


@login_required
def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    contact_list = Cat.published.all()
    paginator = Paginator(contact_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {'title': 'О сайте', 'menu': menu, 'form': form, 'page_obj': page_obj}
    return render(request, 'cats/about.html', data)


class ShowPost(DataMixin, DetailView):
    model = Cat
    template_name = 'cats/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = AddCommentForm()
        return self.get_mixin_context(
            context,
            title=context['post'],
            form_comment=form,
            selected_id=0
        )

    def get_object(self, queryset=None):
        return get_object_or_404(Cat.published, slug=self.kwargs[self.slug_url_kwarg])


def login(request):
    data = {'title': 'О сайте', 'menu': menu}
    return render(request, 'cats/login.html', data)


@permission_required(perm='cats.view_cat', raise_exception=True)
def contacts(request):
    data = {'title': 'О сайте', 'menu': menu}
    return render(request, 'cats/contacts.html', data)


class AddPage(LoginRequiredMixin, PermissionRequiredMixin, DataMixin, CreateView):
    model = Cat
    fields = ['title', 'slug', 'content', 'is_published', 'category']
    template_name = 'cats/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавить статью'
    permission_required = 'cats.add_cat'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


@login_required
def add_comment(request):
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        post = Cat.objects.get(pk=request.POST['post_id'])
        if form.is_valid():
            w = form.save(commit=False)
            w.author = request.user
            w.post = post
            w.save()
        return redirect(post.get_absolute_url())
    else:
        raise Http404("Not found")


@login_required
def like(request):
    if request.method == 'POST':
        post = Cat.objects.get(pk=request.POST['post_id'])
        user = request.user
        l = post.likes.filter(author=user)
        if not l:
            Like.objects.create(author=user, post=post)
            l = post.dislikes.filter(author=user)
            if l:
                l.delete()

        return redirect(post.get_absolute_url())
    else:
        raise Http404("Not found")


@login_required
def dislike(request):
    if request.method == 'POST':
        post = Cat.objects.get(pk=request.POST['post_id'])
        user = request.user
        l = post.dislikes.filter(author=user)
        if not l:
            Dislike.objects.create(author=user, post=post)
            l = post.likes.filter(author=user)
            if l:
                l.delete()

        return redirect(post.get_absolute_url())
    else:
        raise Http404("Not found")


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Cat
    fields = ['title', 'content', 'photo', 'is_published', 'category']
    template_name = 'cats/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактировать статью'
    permission_required = 'cats.update_cat'


class DeletePage(DataMixin, DeleteView):
    model = Cat
    template_name = 'cats/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Удалить статью?'


class CatsCategory(DataMixin, ListView):
    allow_empty = False
    template_name = 'cats/index.html'
    context_object_name = 'cats'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['cats'][0].category
        return self.get_mixin_context(
            context,
            title=f'Рубрика: {category.name}',
            selected_id=category.pk
        )

    def get_queryset(self):
        return Cat.published.filter(category__slug=self.kwargs['category_slug']).select_related('category')


class TagPostList(DataMixin, ListView):
    template_name = 'cats/index.html'
    context_object_name = 'cats'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPosts.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(
            context,
            title=f'Тег: {tag.tag}'
        )

    def get_queryset(self):
        return Cat.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('category')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
