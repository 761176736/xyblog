from django import  forms
from apps.forms import FormMixin
from user.models import User


class LoginForm(forms.Form,FormMixin):
    email = forms.EmailField(error_messages={
        'required':'邮箱不能为空!'
    })
    password = forms.CharField(max_length=16,min_length=6,error_messages={
        'max_length':'密码最多不能超过16位！',
        'min_length':'密码至少有6位！',
        'required':'密码不能为空！'
    })
    remember = forms.IntegerField(required=False)




class RegisterForm(forms.Form,FormMixin):
    email = forms.EmailField(error_messages={
        'required':'邮箱不能为空!'
    })
    username = forms.CharField(max_length=20,error_messages={
        'required':'用户名不能为空!',
    })
    pwd1 = forms.CharField(max_length=16,min_length=6,error_messages={
        "max_length":"密码对多不能超过16位!",
        "min_length":'密码至少6位!',
        'required':'密码不能为空!',
    })
    pwd2 = forms.CharField(max_length=16, min_length=6, error_messages={
        "max_length": "密码对多不能超过16位!",
        "min_length": '密码至少6位!',
        'required':'密码不能为空!'
    })

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        username = cleaned_data.get('username')
        pwd1 = cleaned_data.get('pwd1')
        pwd2 = cleaned_data.get('pwd2')
        email = cleaned_data.get('email')

        if pwd1 != pwd2:
            raise forms.ValidationError('两次密码输入不一致！')

        username_exists = User.objects.filter(email=email).exists()
        exists = User.objects.filter(username=username).exists()

        if username_exists:
            raise forms.ValidationError("该用户名已经存在!")

        if exists:
            raise forms.ValidationError("该邮箱已被注册!")

        return cleaned_data