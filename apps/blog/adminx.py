import xadmin
from .models import Article ,Comment,Category,Tag,Info,ArticleToTag,Likes
from xadmin import views
# Register your models here.

class BaseSetting(object):
    enable_themes = True
    user_bootswatch = True

class GlobalSetting(object):
    site_title = '小雨后台'
    site_footer = '小雨后台'
    menu_style = 'accordion'

class CategoryAdmin(object):
    model_icon='fa fa-paperclip'
    list_display=['name']
xadmin.site.register(Category,CategoryAdmin)

class LikesAdmin(object):
    list_display=['article','user']
xadmin.site.register(Likes,LikesAdmin)


class ArticleAdmin(object):
    model_icon='fa fa-book'
    list_filter=['title','author__username','tags__name','category__name']
    search_fields=['title','author__username','tags__name','category__name']
    list_display = ('title','excerpt','info','category','tags','thumbnail','author','like','comment_num','pub_time')
xadmin.site.register(Article,ArticleAdmin)


class TagAdmin(object):
    model_icon='fa fa-tags'
    search_fields=['name']
    list_display=['name']


xadmin.site.register(Tag,TagAdmin)

class ArticleToTagAdmin(object):
    model_icon='fa fa-tags'
    list_display=['article','tag']
xadmin.site.register(ArticleToTag,ArticleToTagAdmin)

class CommentAdmin(object):
    model_icon='fa fa-comments'
    search_fields=['content','author__username','article__title']
    list_filter = ['content', 'author__username', 'article__title']
    list_display = ['content','author','article','pub_time']
xadmin.site.register(Comment,CommentAdmin)


class InfoAdmin(object):
    model_icon='fa fa-pencil-square-o'
    search_fields=['info']
    list_display=['info']

    class Media:
        js = (
            '/static/kindeditor/kindeditor-all.js',
            '/static/kindeditor/lang/zh_CN.js',
            '/static/kindeditor/config.js',
        )

xadmin.site.register(Info,InfoAdmin)

xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)
