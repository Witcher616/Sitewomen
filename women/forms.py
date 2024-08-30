from django import forms
from .models import Category, Women, Husband


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория',
                                 empty_label="Категория не выбрана")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False,
                                     label='Муж', empty_label="Не замужем")

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 10}),
        }
        labels = {
            'slug': 'URL'
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) <= 3:
            raise forms.ValidationError("Название должно быть длиннее 3 символов")
        elif len(title) > 50:
            raise forms.ValidationError("Название должно быть меньше 50 символов")
        return title


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Файл')
