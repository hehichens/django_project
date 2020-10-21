
"""
forms
"""

from django import forms

from .models import ArticlePost

class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost  # data model source
        fields = ('title', 'body')  # fields contained in the form