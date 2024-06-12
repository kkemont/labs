from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from .models import Cat, Category, TagPosts


for t in [TagPosts]:
    admin.site.register(t)


class HasOwnerFilter(admin.SimpleListFilter):
    title = 'Есть хозяева'
    parameter_name = 'count'

    def lookups(self, request, model_admin):
        return [(True, 'Есть хозяин'),
                (False, 'Нет хозяина')]

    def queryset(self, request, queryset):
        val = self.value()
        if val is None:
            return queryset
        if val == 'True':
            return queryset.filter(owners__count__gt=0)
        else:
            return queryset.filter(owners__count=0)


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ['title', 'slug', 'content', 'photo', 'category', 'tags']
    list_display = ('id', 'title', 'post_photo', 'time_create', 'is_published', 'owners_count')
    list_display_links = ('id', 'title')

    ordering = ['-time_create', 'title']
    list_editable = ('is_published',)
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith', 'category__name']
    list_filter = [HasOwnerFilter, 'category__name', 'is_published']
    filter_horizontal = ['tags']

    @admin.display(description='Изображение')
    def post_photo(self, cat: Cat):
        if cat.photo:
            return mark_safe(f"<img src='{cat.photo.url}' width=50>")
        else:
            return "Без фото"

    @admin.display(description='Наличие владельцев')
    def owners_count(self, cat: Cat):
        return False if cat.owners is None or cat.owners.count == 0 else True

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        cnt = queryset.update(is_published=Cat.Status.PUBLISHED)
        self.message_user(request, f'Опубликовано {cnt} записей')

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        cnt = queryset.update(is_published=Cat.Status.DRAFT)
        self.message_user(request, f'{cnt} записей снято с публикации', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
