#encoding: utf-8
from django.shortcuts import redirect,reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import login,logout,authenticate

from utils import restful
from user.models import User
from .forms import LoginForm,RegisterForm


@csrf_exempt
@require_POST
def login_view(request):
    '''登陆'''
    form = LoginForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request,username=email,password=password)

        if user:
            if user.is_active:
                log=login(request,user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)

                return restful.ok()

            else:
                return restful.unauth(message="该账号已被冻结")
        else:
            return restful.params_error(message='邮箱或者密码错误')

    else:

        errors = form.get_errors()
        return restful.params_error(message=errors)


def logout_view(request):
    '''
    退出登陆
    '''
    logout(request)
    return redirect(reverse("blog:index"))


@csrf_exempt
@require_POST
def register(request):
    '''注册'''
    form = RegisterForm(request.POST)

    if form.is_valid():
        email = form.cleaned_data.get('email')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('pwd1')
        user = User.objects.create_user(username=username,email=email,password=password)
        login(request,user)
        return restful.ok()

    else:
        return restful.params_error(message=form.get_errors())