from django import template
from cats.models import Category, TagPosts

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('cats/list_categories.html')
def show_categories(selected_index=0):
    categories = Category.objects.all()
    return {"cats": categories, "selected_id": selected_index}


@register.inclusion_tag('cats/list_tags.html')
def show_all_tags():
    return {"tags": TagPosts.objects.all()}
