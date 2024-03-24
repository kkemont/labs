from django import template
from cats import views

register = template.Library()


@register.simple_tag()
def get_categories():
    return views.navigation_db


@register.inclusion_tag('cats/list_categories.html')
def show_categories(selected_index=0):
    return {"cats": views.navigation_db, "selected_id": selected_index}
