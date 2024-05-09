from django.urls import path, register_converter
from cats import views, converters
from django.contrib import admin

register_converter(converters.TwoDigitWeightConverter, 'weight2')

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('post/<slug:post_slug>/', views.show_concrete_cat, name='post'),
    path('contact/', views.contacts, name='contacts'),
    path('addpage/', views.add_page, name='add_page'),
    path('login/', views.login, name='login'),
    path('category/<slug:category_slug>/', views.show_categories, name='category'),
    path('tag/<slug:tag_slug>', views.show_tag_posts, name='tag')
]

admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'Мемные коты'
