from django.conf.urls import patterns, url
from ma3ana_kam_app import views


urlpatterns = patterns('',
                       url(r'^expense/new$', views.add_expense, name='add_expense'),
                       url(r'^expense/edit/(?P<pk>\d+)$', views.update_expense, name='update_expense'),
                       url(r'^expense/delete/(?P<pk>\d+)$', views.delete_expense, name='delete_expense'),
                       )