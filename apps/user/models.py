from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model

class UserManager(BaseUserManager):
    def _create_user(self,email,username,password,**kwargs):
        if not email:
            raise ValueError('请传入邮箱！')
        if not username:
            raise ValueError('请传入用户名！')
        if not password:
            raise ValueError('请传入密码！')

        user = self.model(email=email,username=username,**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self,email,username,password,**kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(email,username,password,**kwargs)

    def create_superuser(self,email,username,password,**kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(email,username,password,**kwargs)

class User(AbstractBaseUser,PermissionsMixin):
    # 我们不使用默认的自增长的主键
    # id：100，101，102，103
    email = models.EmailField(unique=True,null=True,verbose_name='邮箱')
    username = models.CharField(max_length=100,verbose_name='用户名')
    nickname = models.CharField(max_length=100, verbose_name='昵称',null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    data_joined = models.DateTimeField(auto_now_add=True,verbose_name='时间')
    intr = models.TextField(max_length=50,null=True,verbose_name='简介')
    avatar = models.ImageField(upload_to='avatar',verbose_name='头像',default="default.png")

    class Meta:
        verbose_name = '用户'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.username


    USERNAME_FIELD = 'email'
    # telephone，username，password
    REQUIRED_FIELDS = ['username']
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

class About(models.Model):
    info = models.TextField(null=True,verbose_name='本人详情')
    user = models.OneToOneField(get_user_model(),on_delete=models.CASCADE,null=True,verbose_name='用户本人',related_name='abouts')

    def __str__(self):
        return self.info

    class Meta:
        verbose_name='本人详情'
        verbose_name_plural=verbose_name