from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'text': 'Текст поста',
            'group': 'Группа',
        }
        help_texts = {
            'text': 'Текст поста',
            'group': 'Группа, к которой относится пост',
        }

    def clean_subject(self):
        text = self.cleaned_data['text']
        if not text:
            raise forms.ValidationError('Ну надо же заполнить текст')
        return text


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'post': 'Пост',
            'author': 'Автор',
            'text': 'Текст комментария',
            'created': 'Дата создания'
        }

    def clean_subject(self):
        text = self.cleaned_data['text']
        if not text:
            raise forms.ValidationError('Ну надо же заполнить текст')
        return text
