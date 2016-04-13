"""fellowms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^fellow/(?P<fellow_id>[0-9]+)/', views.fellow_detail, name="fellow_detail"),
    url(r'^fellow/', views.fellow, name="fellow"),
    url(r'^event/(?P<event_id>[0-9]+)/', views.event_detail, name="event_detail"),
    url(r'^event/', views.event),
    url(r'^expense/(?P<expense_id>[0-9]+)/', views.expense_detail, name="expense_detail"),
    url(r'^expense/', views.expense, name="expense"),
    url(r'^board/', views.board),
    url(r'^admin/', admin.site.urls),
]
