#encoding: utf-8
from django.db.models import F
from django.views.generic import View
from django.shortcuts import render,redirect,reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse,JsonResponse

import os
import json
from bs4 import BeautifulSoup

from utils import restful
from xyblog import settings
from .forms import EmailForm
from user.models import User
from blog.models import Article,Likes,Comment,Info,Category,Tag,ArticleToTag


@csrf_exempt
def like(request):
    user = request.user
    article_id = request.POST.get('article_id')
    article = Article.objects.filter(pk=article_id)
    response= {'state':True}
    try:
        Likes.objects.create(article=article.first(),user=user)
        Article.objects.filter(pk=article_id).update(like=F("like")+1)
    except Exception:
        response['state'] = False
    return JsonResponse(response)

@csrf_exempt
def comment(request):
    '''
    评论
    '''
    article_id = request.POST.get('article_id')
    content = request.POST.get('content')
    pid=request.POST.get('pid')

    user_id = request.user.pk
    response={}

    if not pid:
        comment=Comment.objects.create(article_id=article_id,content=content,author_id=user_id)
    else:
        comment=Comment.objects.create(article_id=article_id,content=content,author_id=user_id,parent_comment_id=pid)

    response['pub_time'] = comment.pub_time
    response['content'] = comment.content
    response['username']=comment.author.username
    response['avatar'] = str(comment.author.avatar)

    return JsonResponse(response)


class Write_article(View):
    '''
    写文章
    '''
    def get(self,request):
        categories = Category.objects.all()
        tags =Tag.objects.all()
        context={
            "categories":categories,
            "tags":tags
        }
        return render(request, 'write.html',context=context)

    def post(self,request):
        title = request.POST.get('title')
        content = request.POST.get('article-content')
        category = request.POST.get('category')
        tags = request.POST.getlist('tag')
        user = request.user
        text = BeautifulSoup(content,"html.parser").text        #将html文本只取字符串
        desc = text[0:100]+'...'
        info = Info.objects.create(info=content)
        category  = Category.objects.filter(name=category).first()
        article = Article.objects.create(title=title,author=user,excerpt=desc,info=info,category=category)

        for tag in tags:
            tag = Tag.objects.get(name=tag)
            ArticleToTag.objects.create(tag=tag,article=article)

        return redirect(reverse('user:write'))


def upload(request):
    obj = request.FILES.get('upload_img')
    path = os.path.join(settings.MEDIA_ROOT,'add_article_img',obj.name)
    with open(path,"wb") as fp:
        for line in obj:
            fp.write(line)
    result = {
        'error':0,
        'url': '/media/add_article_img/'+obj.name
    }
    return HttpResponse(json.dumps(result))


class Person(View):
    def get(self,request,username):
        return render(request,'pseron.html')

@csrf_exempt
@require_POST
def change_email(request):
    '''
    修改邮箱
    '''
    form = EmailForm(request.POST)

    if form.is_valid():
        new_email = form.cleaned_data.get('email')
        print(new_email)
        User.objects.filter(username=request.user.username).update(email=new_email)
        return restful.ok()
    else:
        errors = form.get_errors()
        return restful.params_error(message=errors)

@csrf_exempt
@require_POST
def change_username(request):
    '''
    修改名
    '''
    new_username = request.POST.get('username')
    exists = User.objects.filter(username=new_username).exists()
    if exists:
        return restful.params_error(message="用户名已经存在!")

    User.objects.filter(username=request.user.username).update(username=new_username)
    return restful.ok()


@require_POST
def upload_avatar(request):
    '''
    头像
    '''
    obj = request.FILES.get('file')
    User.objects.filter(username=request.user.username).update(avatar=obj)

    path = os.path.join(settings.MEDIA_ROOT,'avatar',obj.name)        #拼接图片储存路径
    with open(path,"wb") as fp:
        for line in obj:
            fp.write(line)

    result = {
        'error':0,
        'url': '/media/avatar/'+obj.name
    }

    return HttpResponse(json.dumps(result))

