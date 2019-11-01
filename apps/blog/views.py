from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse
from .models import Article,Category,ArticleToTag,Comment,Message
from user.models import User,About
from django.db.models import F,Q
from django.core.paginator import Paginator
from utils import restful

class Index(View):
    '''
    主页
    '''
    def get(self,request):
        page = int(request.GET.get('p', 1))  # 获取页码，默认为第1页
        articles = Article.objects.order_by("-pub_time").all()

        intr = User.objects.filter(pk=1).first().intr
        categories = Category.objects.all()

        paginator = Paginator(articles,7)
        page_obj = paginator.page(page)
        context_data = self.get_pagination_data(paginator,page_obj)

        context = {
            'articles':page_obj.object_list,
            'page_obj':page_obj,
            'categories':categories,
            'intr':intr,
        }

        context.update(context_data)
        return render(request, 'index.html', context=context)

    def get_pagination_data(self, paginator, page_obj, around_count=1):
        current_page = page_obj.number  # 当前页码
        num_pages = paginator.num_pages  # 总页数

        left_has_more = False  # 判断是否有'...'
        right_has_more = False

        if current_page <= around_count + 3:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 2:
            right_pages = range(current_page + 1, num_pages + 1)

        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            'left_pages': left_pages,
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }


def about(request):
    '''
    关于我
    :param request:
    :return:
    '''
    categories = Category.objects.all()

    intr = User.objects.filter(pk=1).first().intr
    info = About.objects.filter(user_id=1).first().info

    context={
        'categories':categories,
        'intr':intr,
        'info':info
    }

    return render(request, 'about.html',context=context)



class  Messages(View):
    '''
    留言
    '''
    def get(self,request):
        categories = Category.objects.all()
        intr = User.objects.filter(pk=1).first().intr
        messages = Message.objects.all()

        context = {
            'categories': categories,
            'intr':intr,
            'messages':messages
        }
        return render(request,'message.html',context=context)

    def post(self,request):
        content = request.POST.get('content')
        user_id = request.user.pk
        Message.objects.create(content=content, author_id=user_id)

        return restful.ok()


def detail(request,username,pk):
    '''
    文章详情
    :param request:
    :param username:
    :param pk:
    :return:
    '''
    user = User.objects.filter(username=username).first()
    article = Article.objects.filter(pk=pk).first()
    categories = Category.objects.all()
    intr = User.objects.filter(pk=1).first().intr

    if article:
        article_views = article.view_num
        article.view_num+=1
        article.save(update_fields=['view_num'])
        previuos = Article.objects.filter(pk=(int(pk)-1)).exists()
        next = Article.objects.filter(pk=(int(pk)+1)).exists()
        tags = ArticleToTag.objects.filter(article=article).values('tag__name')
        comments = Comment.objects.filter(article_id=pk).all()
        comment_count = comments.count()

        context = {
            'username':username,
            'article':article,
            'tags':tags,
            'comments':comments,
            'article_views':article_views,
            'comment_count':comment_count,
            'previous':previuos,
            'next':next,
            'categories':categories,
            'intr':intr,
        }
        return render(request, 'detail.html', context=context)

    else:
        return render(request,'404.html')



def log_page(request):
    '''登陆页面'''
    return render(request,'login.html')



def comments(request, article_id):
    '''
    评论列表
    :param request:
    :param article_id:
    :return:
    '''
    ret = list(Comment.objects.filter(article_id=article_id).values('pk', 'content', 'parent_comment_id','author'))
    return JsonResponse(ret, safe=False)



def search(request):
    '''
    搜索
    :param request:
    :return:
    '''
    q = request.GET.get('search-text')
    categories = Category.objects.all()
    intr = User.objects.filter(pk=1).first().intr

    if not q:
        return render(request,'search.html',context={"error":"请输入关键字","categories":categories,'intr':intr})
    else:
        articles = Article.objects.filter(Q(title__icontains=q)|Q(info__info__icontains=q)).order_by("-pub_time").all()

        if len(articles) == 0:
            return render(request, 'search.html', context={"message":'没有找到内容，换个关键词搜搜?','intr':intr})
        else:
            context={
                'articles':articles,
                'categories':categories,
                'intr':intr
            }
            return render(request,'search.html',context=context)




def category_list(request,category):
    '''
    分类列表
    '''
    articles = Article.objects.filter(category__name=category)
    categories = Category.objects.all()

    context = {
        'articles':articles,
        'categories':categories
    }

    return render(request,'caregory.html',context=context)

