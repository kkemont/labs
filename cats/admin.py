from django.contrib import admin, messages

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
    fields = ['title', 'slug', 'content', 'category', 'tags']
    list_display = ('id', 'title', 'time_create', 'is_published', 'brief_info')
    list_display_links = ('id', 'title')
    ordering = ['-time_create', 'title']
    list_editable = ('is_published',)
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith', 'category__name']
    list_filter = [HasOwnerFilter, 'category__name', 'is_published']
    filter_horizontal = ['tags']

    @admin.display(description='Размер описания')
    def brief_info(self, cat: Cat):
        return f'Описание {len(cat.content)} символов'

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
