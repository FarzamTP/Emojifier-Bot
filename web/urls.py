from django.conf.urls import url
from . import views

urlpatterns = [
    url('^api/ask$', views.classify, name='index'),
    url('^api/submit$', views.submit, name='submit'),
    url('^api/export$', views.export_to_csv, name='export_to_csv'),
]