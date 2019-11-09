from .models import User


def about_context_processors(request):
    context = {}
    try:
        user = User.objects.get(pk=1)
        context['myintr'] = user.intr
        context['myname'] = user.username
    except:
        pass
    return context