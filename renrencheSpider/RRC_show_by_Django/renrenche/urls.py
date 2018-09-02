
from django.conf.urls import url
from renrenche import views


urlpatterns = [
    url(r'^rrc/$', views.index, name='index'),
    url(r'^1/$', views.index1, name='1'),
    url(r'^2/$', views.index2, name='2'),
    url(r'^3/$', views.index3, name='3'),
    url(r'^4/$', views.index4, name='4'),
    url(r'^5/$', views.index5, name='5'),
    url(r'^6/$', views.index6, name='6'),
]
