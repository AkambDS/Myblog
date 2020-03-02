from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . views import (
    PostListView, PostDetailView,
    PostCreateView)

urlpatterns = [

    url(r'^register/$', views.register, name='register'),
    url(r'^updateprofile/$', views.profile, name='profile'),
    url(r'^$', PostListView.as_view(), name='home'),
    url(r'^(?P<id>[0-9]+)/$', PostDetailView.as_view(), name='profile-detail'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='my_userauth/loginuser.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(
        template_name='my_userauth/logout.html'), name='logout'),
    url('profile/new/', PostCreateView.as_view(), name='post-create')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


# class based view loks for template in <app>/<model>_<viewtype>.html
