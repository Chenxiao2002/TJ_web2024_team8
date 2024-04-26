from django import forms
from .models import Blog, BlogType
from ckeditor.widgets import CKEditorWidget

class BlogForm(forms.Form):
    text=forms.CharField(widget=CKEditorWidget(config_name='blog_ckeditor'))