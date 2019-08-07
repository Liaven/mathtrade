from django.conf.urls import url
#from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    url(r'^$', views.index, name='index'),
    url(r'showtrade/(?P<pk>[0-9]+)/$', views.ShowTrade, name='player-showtrade'),
    url(r'wantlist/', views.ShowWants , name='wantlist'),
    url(r'exectrade/', views.ExecTrade, name='exectrade'),
]

