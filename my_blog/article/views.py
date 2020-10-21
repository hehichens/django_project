"""
@hichens
"""


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
import markdown

from .models import ArticlePost
from .forms import ArticlePostForm
from comment.models import Comment

# Create your views here.

"""show the articles"""
def article_list(request):

    search = request.GET.get('search')
    order = request.GET.get('order')

    if search:
        if request.GET.get('order') == 'total_view':
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_view')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        search = ''
        if order == 'total_view':
            article_list = ArticlePost.objects.all().order_by('-total_view')
        else:
            article_list = ArticlePost.objects.all()

    paginator = Paginator(article_list, 2)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = {'articles': articles, 'order': order, 'search': search}
    return render(request, 'article/list.html', context)


"""show the article detail"""
def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    comments = Comment.objects.filter(article=id)

    article.total_view += 1
    article.save(update_fields=['total_view'])
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)
    context = {'article': article, 'toc': md.toc, 'comments': comments}

    return render(request, 'article/detail.html', context)

"""write article"""
def article_create(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            new_article.save()
            return redirect('article:article_list')
        else:
            return HttpResponse("表单错误, 请重新填写")

    else:
        article_post_form = ArticlePostForm()
        context = {'article_post_form': article_post_form}
        return render(request, 'article/create.html', context)


"""delete article safely"""
def article_safe_delete(request, id):
    if request.method == "POST":
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse('仅允许post请求')


"""update article"""
def article_update(request, id):
    article = ArticlePost.objects.get(id=id)

    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章")

    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        new_article = request.POST
        if article_post_form.is_valid():
            article.title = new_article['title']
            article.body = new_article['body']
            article.save()
            return redirect('article:article_detail', id=id)
        else:
            return HttpResponse("表单错误, 请重新填写")

    else:
        article_post_form = ArticlePostForm()
        context = {
            'article': article,
            'article_post_form': article_post_form,
        }
        return render(request, 'article/update.html', context)

