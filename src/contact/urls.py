from django.conf.urls import url
from django.contrib import admin

from .views import (
  home_page,
  about_page,
  contact_form,
  contact_thanks,
  contact_join,
  contact_jointhanks,
  contact_unsubscribe,
  )

urlpatterns = [
    url(r'^form/$', contact_form, name='contact'),
    url(r'^about/$', about_page, name='about'),
    url(r'^thanks/$', contact_thanks, name='cthanks'),
    url(r'^subscribe/$', contact_join, name='join'),
    url(r'^subscribe/thanks/$', contact_jointhanks, name='thanks'),
    url(r'^unsubscribe/success/$', contact_unsubscribe, name='unsubscribe'),
    url(r'^$', home_page, name='home'),
]
