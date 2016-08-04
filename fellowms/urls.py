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
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

from . import views
from . import settings 

urlpatterns = [
    url(r'^sign_in/', auth_views.login,
        {'template_name': 'fellowms/sign_in.html'},
        name="sign_in"),
    url(r'^sign_out/', auth_views.logout,
        {'next_page': '/'},
        name="sign_out"),
    url(r'^fellow/(?P<fellow_id>[0-9]+)/', views.fellow_detail, name="fellow_detail"),
    url(r'^fellow/', views.fellow, name="fellow"),
    url(r'^event/(?P<event_id>[0-9]+)/review', views.event_review, name="event_review"),
    url(r'^event/(?P<event_id>[0-9]+)/', views.event_detail, name="event_detail"),
    url(r'^event/previous/', views.event_past, name="event_past"),
    url(r'^event/', views.event, name="event"),
    url(r'^expense/(?P<expense_id>[0-9a-z\-]+)/review', views.expense_review, name="expense_review"),
    url(r'^expense/(?P<expense_id>[0-9a-z\-]+)/', views.expense_claim, name="expense_claim"),
    url(r'^expense/', views.expense, name="expense"),
    url(r'^blog/(?P<blog_id>[0-9]+)/review', views.blog_review, name="blog_review"),
    url(r'^blog/(?P<blog_id>[0-9]+)/', views.blog_detail, name="blog_detail"),
    url(r'^blog/', views.blog, name="blog"),
    url(r'^dashboard/', views.dashboard, name="dashboard"),
    url(r'^geojson/', views.geojson, name="geojson"),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name="index"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
