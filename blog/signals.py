
from django.core.cache import cache
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(user_logged_in)
def user_login(sender,user,request,**kwargs):
    ip = request.META.get('REMOTE_ADDR')
    request.session['ip'] = ip
    ct = cache.get('count',0,version=user.pk)
    newcount = ct+1
    cache.set('count',newcount,60*60,version=user.pk)
