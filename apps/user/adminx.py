import xadmin
from .models import User,About
# Register your models here.


class AboutAdmin(object):
    model_icon='fa fa-info'
    list_display=('info','user')
xadmin.site.register(About,AboutAdmin)


class UserAdmin(object):
    model_icon='fa fa-user'
    list_display = ('username','email','password','data_joined','avatar','intr','is_staff','is_active')
xadmin.site.unregister(User)
xadmin.site.register(User,UserAdmin)


