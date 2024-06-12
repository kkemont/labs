from django.urls import path, register_converter
from cats import views, converters
from django.contrib import admin

register_converter(converters.TwoDigitWeightConverter, 'weight2')

urlpatterns = [
    path('', views.CatsHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('edit/<slug:slug>', views.UpdatePage.as_view(), name='edit_page'),
    path('delete/<slug:slug>', views.DeletePage.as_view(), name='delete_page'),
    path('contact/', views.contacts, name='contacts'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('login/', views.login, name='login'),
    path('category/<slug:category_slug>/', views.CatsCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>', views.TagPostList.as_view(), name='tag'),
    path('comment/', views.add_comment, name='comment'),
    path('like/', views.like, name='like'),
    path('dislike/', views.dislike, name='dislike'),
]

admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'Мемные коты'

