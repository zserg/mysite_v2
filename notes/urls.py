from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$',                 views.IndexView.as_view(), name='index'),
        url(r'^post/$',            views.PostNoteView.as_view(), name='post'),
        url(r'^([_0-9A-Za-z]+)/$', views.NoteView.as_view(), name='note'),
        url(r'^delete/([_0-9A-Za-z]+)/$', views.DeleteNoteView.as_view(), name='delete'),
]
