from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from .views import Login, CreateAuth

urlpatterns = [
    url(r'^users/login/$', Login.as_view()),
    url(r'^users/login/(?P<name>\w{0,50})/$', Login.as_view()),
    url(r'^users/create/$', CreateAuth.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)
