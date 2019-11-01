from django import forms
from forms import FormMixin
from .models import User

class EmailForm(forms.Form,FormMixin):
    email = forms.EmailField(error_messages={
        'required': '邮箱不能为空!'
    })

    def clean(self):
        cleaned_data = super(EmailForm, self).clean()
        new_email = cleaned_data.get('email')
        exists = User.objects.filter(email=new_email).exists()

        if exists:
            raise forms.ValidationError("该邮箱已被注册!")

        return cleaned_data
