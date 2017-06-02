from django.conf.urls import url
from introduction import views

urlpatterns = [
    url(r'^$', views.ml_index, name='ml_index'),
    url(r'^machine_learning/$', views.ml, name='ml'),
    url(r'^problems/$', views.problems, name='problems'),
    url(r'^tasks/$', views.tasks, name='tasks'),
]

