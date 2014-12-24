from django.conf.urls import patterns, include, url
from django.contrib import admin
from ma3ana_kam_app import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='home'),
                       url(r'^expense/new$', views.add_expense, name='add_expense'),
                       url(r'^expense/edit/(?P<pk>\d+)$', views.update_expense, name='update_expense'),
                       url(r'^expense/delete/(?P<pk>\d+)$', views.delete_expense, name='delete_expense'),
                       url(r'^period/new$', views.add_period, name='add_period'),
                       url(r'^period/edit/(?P<pk>\d+)$', views.update_period, name='update_period'),
                       url(r'^period/delete/(?P<pk>\d+)$', views.delete_period, name='delete_period'),
                       url(r'^period/list/(?P<index_number>\d+)/(?P<page_size>\d+)/$', views.period_list,
                           name='period_list'),
                       url(r'^admin/', include(admin.site.urls)),

                       )
