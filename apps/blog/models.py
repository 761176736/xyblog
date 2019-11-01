from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    '''分类'''
    name = models.CharField(max_length=100,verbose_name='分类')
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Tag(models.Model):
    '''标签'''
    name = models.CharField(max_length=100,verbose_name='标签')
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=100,verbose_name='标题')
    pub_time = models.DateTimeField(auto_now_add=True,verbose_name='更改时间')
    excerpt = models.CharField(max_length=200,blank=True,verbose_name='摘要') #摘要
    category = models.ForeignKey(Category,null=True,on_delete=models.DO_NOTHING,verbose_name='分类')
    # tags = models.ManyToManyField("Tag",blank=True,verbose_name='标签')
    thumbnail = models.CharField(max_length=32,null=True,verbose_name='缩略图')
    like = models.IntegerField(null=True,default=0,verbose_name='点赞')
    comment_num=models.IntegerField(null=True,default=0,verbose_name='评论')

    view_num = models.PositiveIntegerField(default=0,verbose_name='浏览量')

    info = models.OneToOneField('Info',on_delete=models.CASCADE,verbose_name='文章详情')
    author = models.ForeignKey(get_user_model(),on_delete=models.SET_NULL,null=True,verbose_name='作者')
    tags = models.ManyToManyField("Tag", through="ArticleToTag",blank=True, verbose_name='标签')

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


# 文章和标签关系表 中介表
class ArticleToTag(models.Model):
    article = models.ForeignKey('Article',verbose_name='文章',on_delete=models.CASCADE,null=True)
    tag = models.ForeignKey('Tag',verbose_name='标签',on_delete=models.CASCADE,null=True)
    class Meta:
        verbose_name='文章和标签关系表'
        verbose_name_plural=verbose_name
        unique_together = [
            ("article","tag")
        ]
    def __str__(self):
        return self.article.title + ' ' + self.tag.name


class Info(models.Model):
    info = models.TextField(verbose_name='文章详情')
    class Meta:
        verbose_name = "文章详情"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.info


class Comment(models.Model):
    content = models.TextField(verbose_name='内容')
    pub_time = models.DateTimeField(auto_now_add=True,verbose_name='更新时间')
    article = models.ForeignKey('Article',on_delete=models.CASCADE,related_name='comments',verbose_name='文章')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,verbose_name='作者')
    parent_comment = models.ForeignKey('self',null=True,verbose_name='父评论',on_delete=models.CASCADE)
    class Meta:
        verbose_name ='评论'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.content





class Message(models.Model):
    content = models.TextField(verbose_name='内容')
    pub_time = models.DateTimeField(auto_now_add=True,verbose_name='更新时间')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,verbose_name='作者')
    class Meta:
        verbose_name ='留言'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.content


#点赞记录
class Likes(models.Model):
    user = models.ForeignKey(get_user_model(),null=True,on_delete=models.CASCADE,verbose_name='点赞用户')
    article = models.ForeignKey('Article',null=True,on_delete=models.CASCADE,verbose_name='点赞文章')

    def __str__(self):
        return self.user

    class Meta:
        unique_together=(("article","user"),)
        verbose_name="文章点赞"
        verbose_name_plural=verbose_name
