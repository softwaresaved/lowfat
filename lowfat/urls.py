"""lowfat path Configuration

The `pathpatterns` list routes paths to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/paths/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a path to pathpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a path to pathpatterns:  path('', Home.as_view(), name='home')
Including another pathconf
    1. Import the include() function: from django.conf.paths import path, include
    2. Add a path to pathpatterns:  path('blog/', include('blog.paths'))
"""
from django.conf.urls import include, url, path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

from . import views
from . import settings

admin.site.site_header = "lowFAT administration"
admin.site.site_title = "lowFAT administration"
admin.site.index_title = "lowFAT administration"
admin.site.login_template = "lowfat/admin_login.html"

STAFF_PATTERNS = [
    path('photos/', views.get_fellows_photos, name="get_fellows_photos"),
    path('rss/', views.rss, name="rss"),
    path('', views.staff, name="staff"),
]


CLAIMED_PATTERNS = [
    path('<int:claimant_id>/promote/', views.claimant_promote, name="claimant_promote"),
    path('<int:claimant_id>/demote/', views.claimant_demote, name="claimant_demote"),
    path('<int:claimant_id>/', views.claimant_detail, name="claimant_detail"),
    path('<slug:claimant_slug>/', views.claimant_slug_resolution, name="claimant_slug"),
    path('', views.claimant_form, name="claimant"),
]

FELLOW_PATTERNS = [
    path('<int:claimant_id>/promote/', views.claimant_promote, name="fellow_promote"),
    path('<int:claimant_id>/demote/', views.claimant_demote, name="fellow_demote"),
    path('<int:claimant_id>/', views.claimant_detail, name="fellow_detail"),
    path('<slug:claimant_slug>/', views.claimant_slug_resolution, name="fellow_slug"),
    path('', views.claimant_form, name="fellow"),
]

FUND_PATTERNS = [
    path('<int:fund_id>/expense/<int:expense_relative_number>/?', views.expense_detail_relative, name="expense_detail_relative"),
    path('<int:fund_id>/expense/<int:expense_relative_number>/review', views.expense_review_relative, name="expense_review_relative"),
    path('<int:fund_id>/expense/<int:expense_relative_number>/edit', views.expense_edit_relative, name="expense_edit_relative"),
    path('<int:fund_id>/expense/<int:expense_relative_number>/remove', views.expense_remove_relative, name="expense_remove_relative"),
    path('<int:fund_id>/expense/<int:expense_relative_number>/append', views.expense_append_relative, name="expense_append_relative"),
    path('<int:fund_id>/expense/<int:expense_relative_number>/pdf', views.expense_claim_relative, name="expense_claim_relative"),
    path('<int:fund_id>/review', views.fund_review, name="fund_review"),
    path('<int:fund_id>/edit', views.fund_edit, name="fund_edit"),
    path('<int:fund_id>/remove', views.fund_remove, name="fund_remove"),
    path('<int:fund_id>/', views.fund_detail, name="fund_detail"),
    path('previous/', views.fund_past, name="fund_past"),
    path('ical/<token>/', views.fund_ical, name="fund_ical"),
    path('import/', views.fund_import, name="fund_import"),
    path('', views.fund_form, name="fund"),
]

urlpatterns = [  # pylint: disable=invalid-name
    path('login/reset/', auth_views.password_reset,
         {
             'template_name': 'lowfat/password_reset.html',
             'email_template_name': 'lowfat/password_reset_email.html',
             'subject_template_name': 'lowfat/password_reset_subject.txt',
         },
         name="password_reset"),
    path('login/reset/done/', auth_views.password_reset_done,
         {'template_name': 'lowfat/password_reset_done.html'},
         name="password_reset_done"),
    path('login/reset/<uidb64>/<token>/', auth_views.password_reset_confirm,
         {'template_name': 'lowfat/password_reset_confirm.html'},
         name="password_reset_confirm"),
    path('login/reset/complete/', auth_views.password_reset_complete,
         {'template_name': 'lowfat/password_reset_complete.html'},
         name="password_reset_complete"),
    path('', include('social_django.urls', namespace='social')),
    path('login/', auth_views.login,
         {'template_name': 'lowfat/sign_in.html'},
         name="sign_in"),
    path('disconnect/', auth_views.logout,
         {'next_page': '/'},
         name="sign_out"),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('claimant/', include(CLAIMED_PATTERNS)),
    path('fellow/', include(FELLOW_PATTERNS)),
    path('request/', include(FUND_PATTERNS)),
    path('public/request/<access_token>/expense/', views.expense_form_public, name="expense_form_public"),
    path('public/request/<access_token>/blog/', views.blog_form_public, name="blog_form_public"),
    path('public/request/<access_token>/', views.fund_detail_public, name="fund_detail_public"),
    path('public/request/', views.fund_form_public, name="fund_public"),
    path('public/expense/<access_token>/', views.expense_detail_public, name="expense_detail_public"),
    path('public/expense/<access_token>/pdf/', views.expense_claim_public, name="expense_claim_public"),
    path('public/blog/<access_token>/', views.blog_detail_public, name="blog_detail_public"),
    path('fund/', include(FUND_PATTERNS, "lowfat", "fund_")),
    path('expense/<int:expense_id>/pdf', views.expense_claim, name="expense_claim"),
    path('expense/<int:expense_id>/review', views.expense_review, name="expense_review"),
    path('expense/<int:expense_id>/', views.expense_detail, name="expense_detail"),
    path('expense/', views.expense_form, name="expense"),
    path('blog/<int:blog_id>/review', views.blog_review, name="blog_review"),
    path('blog/<int:blog_id>/edit', views.blog_edit, name="blog_edit"),
    path('blog/<int:blog_id>/remove', views.blog_remove, name="blog_remove"),
    path('blog/<int:blog_id>/', views.blog_detail, name="blog_detail"),
    path('blog/', views.blog_form, name="blog"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('promote/', views.promote, name="promote"),
    path('my-profile/', views.my_profile, name="my_profile"),
    path('geojson/', views.geojson, name="geojson"),
    path('report/<report_filename>/', views.report_by_name, name="report_by_name"),
    path('report/', views.report, name="report"),
    path('search/', views.search, name="search"),
    path('recent-actions/', views.recent_actions, name="recent_actions"),
    path('staff/', include(STAFF_PATTERNS)),
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
