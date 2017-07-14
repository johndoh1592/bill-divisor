# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from divisor import views as divisor_views

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', divisor_views.StartView.as_view(), name='home'),


    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),


    url(r'^events/(?P<event_id>\d+)/$', divisor_views.detail_event, name='detail_event'),
    url(r'^events/create/$', divisor_views.create_event, name='create_event'),
    url(r'^events/(?P<event_id>\d+)/edit/', divisor_views.edit_event, name='edit_event'),
    url(r'^events/(?P<event_id>\d+)/delete/', divisor_views.delete_event, name='remove_event'),


    url(r'events/(?P<event_id>\d+)/consuming-groups/(?P<consuming_group_id>\d+)/$',
        divisor_views.detail_consuming_group, name='detail_consuming_group'),
    url(r'events/(?P<event_id>\d+)/consuming-groups/create/', divisor_views.create_consuming_group,
        name='create_consuming_group'),
    url(r'events/(?P<event_id>\d+)/consuming-groups/(?P<consuming_group_id>\d+)/edit/',
        divisor_views.edit_consuming_group, name='edit_consuming_group'),
    url(r'events/(?P<event_id>\d+)/consuming-groups/(?P<consuming_group_id>\d+)/delete/',
        divisor_views.delete_consuming_group, name='remove_consuming_group'),
    url(r'events/(?P<event_id>\d+)/consuming-groups/(?P<consuming_group_id>\d+)/delete-participant/$',
        divisor_views.delete_consuming_group_participant, name='remove_consuming_group_participant'),


    url(r'events/(?P<event_id>\d+)/participants/(?P<participant_id>\d+)/$',
        divisor_views.detail_participant, name='detail_participant'),
    url(r'events/(?P<event_id>\d+)/participants/create/', divisor_views.create_participant,
        name='create_participant'),
    url(r'events/(?P<event_id>\d+)/participants/(?P<participant_id>\d+)/edit/',
        divisor_views.edit_participant, name='edit_participant'),
    url(r'events/(?P<event_id>\d+)/participants/(?P<participant_id>\d+)/delete/',
        divisor_views.delete_participant, name='remove_participant'),


    url(r'^events/(?P<event_id>\d+)/bills/(?P<bill_id>\d+)/$', divisor_views.detail_bill, name='detail_bill'),
    url(r'events/(?P<event_id>\d+)/bills/create/', divisor_views.create_bill, name='create_bill'),
    url(r'^events/(?P<event_id>\d+)/bills/(?P<bill_id>\d+)/edit/', divisor_views.edit_bill, name='edit_bill'),
    url(r'^events/(?P<event_id>\d+)/bills/(?P<bill_id>\d+)/delete/', divisor_views.delete_bill, name='remove_bill'),


    url(r'^events/(?P<event_id>\d+)/bills/(?P<bill_id>\d+)/participants/(?P<bill_participant_id>\d+)/$',
        divisor_views.detail_bill_participant, name='detail_bill_participant'),
    url(r'events/(?P<event_id>\d+)/bills/(?P<bill_id>\d+)/participants/create/', divisor_views.create_bill_participant,
        name='create_bill_participant'),
    url(r'^events/(?P<event_id>\d+)/bills/(?P<bill_id>\d+)/participants/(?P<bill_participant_id>\d+)/edit/',
        divisor_views.edit_bill_participant, name='edit_bill_participant'),
    url(r'^events/(?P<event_id>\d+)/bills/(?P<bill_id>\d+)/participants/(?P<bill_participant_id>\d+)/delete/',
        divisor_views.delete_bill_participant, name='remove_bill_participant'),


    url(r'^events/(?P<event_id>\d+)/bills/(?P<bill_id>\d+)/positions/(?P<bill_position_id>\d+)/$',
        divisor_views.detail_bill_position, name='detail_bill_position'),
    url(r'events/(?P<event_id>\d+)/bills/(?P<bill_id>\d+)/positions/create/', divisor_views.create_bill_position,
        name='create_bill_position'),
    url(r'^events/(?P<event_id>\d+)/bills/(?P<bill_id>\d+)/positions/(?P<bill_position_id>\d+)/edit/',
        divisor_views.edit_bill_position, name='edit_bill_position'),
    url(r'^events/(?P<event_id>\d+)/bills/(?P<bill_id>\d+)/positions/(?P<bill_position_id>\d+)/delete/',
        divisor_views.delete_bill_position, name='remove_bill_position'),

]
