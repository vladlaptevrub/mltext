from django.conf.urls import url
from python import views

urlpatterns = [
    url(r'^$', views.py_index, name='py_index'),
    url(r'^hello/$', views.hello, name='hello'),
    url(r'^introduction/$', views.introduction, name='introduction'),
    url(r'^pandas/$', views.pandas, name='pandas'),
]

