from django.conf.urls import url
from naive_b import views

urlpatterns = [
    url(r'^$', views.nb_index, name='nb_index'),
    url(r'^dataset/$', views.dataset, name='dataset'),
    url(r'^tokenization/$', views.tokenization, name='tokenization'),
    url(r'^normalization/$', views.normalization, name='normalization'),
    url(r'^features/$', views.features, name='features'),
    url(r'^classifier/$', views.classifiers, name='classifiers'),
    url(r'^result/$', views.result, name='result'),
    url(r'^test/$', views.test, name='test'),
    url(r'^test_get/$', views.test_get, name='test_get'),
    url(r'^post_test_data/$', views.post_test_data, name='post_test_data'),
    url(r'^delete_test_data/$', views.delete_test_data, name='delete_test_data'),
    url(r'^delete_class_data/$', views.delete_class_data, name='delete_class_data'),
    url(r'^get_history/$', views.get_history, name='get_history'),
]

