"""lowfat URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

from . import views
from . import settings

CLAIMED_PATTERNS = [
    url(r'^(?P<claimant_id>[0-9]+)/promote/', views.claimant_promote, name="claimant_promote"),
    url(r'^(?P<claimant_id>[0-9]+)/', views.claimant_detail, name="claimant_detail"),
    url(r'^(?P<claimant_slug>.+)/', views.claimant_slug_resolution, name="claimant_slug"),
    url(r'^', views.claimant_form, name="claimant"),
]

FELLOW_PATTERNS = [
    url(r'^(?P<claimant_id>[0-9]+)/promote/', views.claimant_promote, name="fellow_promote"),
    url(r'^(?P<claimant_id>[0-9]+)/', views.claimant_detail, name="fellow_detail"),
    url(r'^(?P<claimant_slug>.+)/', views.claimant_slug_resolution, name="fellow_slug"),
    url(r'^', views.claimant_form, name="fellow"),
]

FUND_PATTERNS = [
    url(r'^(?P<fund_id>[0-9]+)/expense/(?P<expense_relative_number>[0-9\-]+)/review', views.expense_review_relative, name="expense_review_relative"),
    url(r'^(?P<fund_id>[0-9]+)/expense/(?P<expense_relative_number>[0-9\-]+)/', views.expense_detail_relative, name="expense_detail_relative"),
    url(r'^(?P<fund_id>[0-9]+)/review', views.fund_review, name="fund_review"),
    url(r'^(?P<fund_id>[0-9]+)/', views.fund_detail, name="fund_detail"),
    url(r'^previous/', views.fund_past, name="fund_past"),
    url(r'^import/', views.fund_import, name="fund_import"),
    url(r'^', views.fund_form, name="fund"),
]

urlpatterns = [  # pylint: disable=invalid-name
    url(r'^login/reset/$', auth_views.password_reset,
        {
            'template_name': 'lowfat/password_reset.html',
            'email_template_name': 'lowfat/password_reset_email.html',
            'subject_template_name': 'lowfat/password_reset_subject.txt',
        },
        name="password_reset"),
    url(r'^login/reset/done/?$', auth_views.password_reset_done,
        {'template_name': 'lowfat/password_reset_done.html'},
        name="password_reset_done"),
    url(r'^login/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/?$', auth_views.password_reset_confirm,
        {'template_name': 'lowfat/password_reset_confirm.html'},
        name="password_reset_confirm"),
    url(r'^login/reset/complete/?$', auth_views.password_reset_complete,
        {'template_name': 'lowfat/password_reset_complete.html'},
        name="password_reset_complete"),
    url('', include('social_django.urls', namespace='social')),
    url(r'^login/$', auth_views.login,
        {'template_name': 'lowfat/sign_in.html'},
        name="sign_in"),
    url(r'^disconnect/', auth_views.logout,
        {'next_page': '/'},
        name="sign_out"),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^claimant/', include(CLAIMED_PATTERNS)),
    url(r'^fellow/', include(FELLOW_PATTERNS)),
    url(r'^request/', include(FUND_PATTERNS)),
    url(r'^fund/', include(FUND_PATTERNS, "lowfat", "fund_")),
    url(r'^expense/(?P<expense_id>[0-9\-]+)/review', views.expense_review, name="expense_review"),
    url(r'^expense/(?P<expense_id>[0-9\-]+)/', views.expense_detail, name="expense_detail"),
    url(r'^expense/', views.expense_form, name="expense"),
    url(r'^blog/(?P<blog_id>[0-9]+)/review', views.blog_review, name="blog_review"),
    url(r'^blog/(?P<blog_id>[0-9]+)/delete', views.blog_delete, name="blog_delete"),
    url(r'^blog/(?P<blog_id>[0-9]+)/', views.blog_detail, name="blog_detail"),
    url(r'^blog/', views.blog_form, name="blog"),
    url(r'^dashboard/', views.dashboard, name="dashboard"),
    url(r'^promote/', views.promote, name="promote"),
    url(r'^my-profile/', views.my_profile, name="my_profile"),
    url(r'^geojson/', views.geojson, name="geojson"),
    url(r'^report/', views.report, name="report"),
    url(r'^search/', views.search, name="search"),
    url(r'^recent-actions/', views.recent_actions, name="recent_actions"),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name="index"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
