from django.conf.urls import url
from pycompiler import views

urlpatterns = [
    url(r'^$', views.pc_index, name='pc_index'),
]

