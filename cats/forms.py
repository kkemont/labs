from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator, deconstructible, ValidationError
from .models import Category, Owners, Cat, Comment


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789 -'
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Должный присутствовать только русские символы, дефис и пробел.'

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code, params={'value': value})


class AddPostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label='Категория не выбрана', label='Категория')
    owners = forms.ModelChoiceField(queryset=Owners.objects.all(), required=False,
                                    empty_label='Нет хозяев', label='Хозяева')

    class Meta:
        model = Cat
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'category', 'owners', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 5})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title


class UploadFileForm(forms.Form):
    file = forms.ImageField(label='Изображение')


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': 'Комментировать'}
        widgets = {'content': forms.Textarea(attrs={'cols': 90, 'rows': 5})}
