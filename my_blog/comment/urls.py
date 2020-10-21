


from django.urls import path

from . import views

app_name = 'article'

"""save the url paths"""
urlpatterns = [
    path('post-comment/<int:article_id>', views.post_comment, name='post_comment')
]