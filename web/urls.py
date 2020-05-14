from django.conf.urls import url
from . import views

urlpatterns = [
    url('^api/ask$', views.classify, name='index'),
]