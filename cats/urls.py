from django.urls import path, register_converter
from cats import views, converters

register_converter(converters.TwoDigitWeightConverter, 'weight2')

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('cats/<int:cat_id>/', views.show_concrete_cat, name='cats'),
    path('contact/', views.contacts, name='contacts'),
    path('addpage/', views.add_page, name='add_page'),
    path('login/', views.login, name='login'),
    path('filter/<int:filter_id>/', views.show_categories, name='filter'),
]
