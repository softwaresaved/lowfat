import copy
import os

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from lowfat.models import Blog, Claimant, Expense, Fund, FUND_STATUS_APPROVED_SET, BlogSentMail
from lowfat.forms import BlogForm, BlogReviewForm
from lowfat.mail import blog_review_notification, new_blog_notification

User = get_user_model()


@login_required
def blog_form(request, **kargs):  # pylint: disable=too-many-branches
    # Setup Blog to edit if provide
    if "blog_id" in kargs:
        try:
            blog_to_edit = Blog.objects.get(id=kargs["blog_id"])
        except:  # pylint: disable=bare-except
            blog_to_edit = None
            messages.error(request, "The blog that you want to edit doesn't exist.")
    else:
        blog_to_edit = None
    # Setup Fund if provided
    fund_id = request.GET.get("fund_id")
    if fund_id:
        fund = Fund.objects.get(id=fund_id)
        initial = {"fund": fund}
    else:
        fund = None
        initial = {}

    formset = BlogForm(
        request.POST or None,
        request.FILES or None,
        instance=blog_to_edit,
        initial=None if blog_to_edit else initial,
        is_staff=bool(request.user.is_staff)
    )

    if formset.is_valid():
        blog = formset.save()

        # Save information about success
        if blog.fund:
            blog.fund.success_reported = formset.cleaned_data["success_reported"]
            blog.fund.save()

        # Handle blog post not related with a funding request
        if not blog.author:
            if formset.cleaned_data["author"]:  # Because blog.author is None!
                blog.author = Claimant.objects.get(id=formset.cleaned_data["author"])
            elif blog.fund:
                blog.author = blog.fund.claimant
            elif not request.user.is_staff:
                blog.author = Claimant.objects.get(user=request.user)
            else:
                blog.delete()  # XXX Quick way to solve the issue
                messages.error(request, 'Blog post not saved. Please provide a author.')
                return HttpResponseRedirect(
                    reverse('blog')
                )
        blog.save()

        messages.success(request, 'Blog draft saved.')
        if not formset.cleaned_data["not_send_email_field"]:
            new_blog_notification(blog)
        return HttpResponseRedirect(
            reverse('blog_detail', args=[blog.id])
        )

    # Limit dropdown list to claimant
    if not request.user.is_staff:
        try:
            claimant = Claimant.objects.get(user=request.user)
        except:  # pylint: disable=bare-except
            return HttpResponseRedirect(reverse('django.contrib.flatpages.views.flatpage', kwargs={'url': '/unavailable/'}))
        formset.fields["fund"].queryset = Fund.objects.filter(
            claimant=claimant,
            status__in=FUND_STATUS_APPROVED_SET
        )
    elif request.GET.get("claimant_id"):
        claimant = Claimant.objects.get(id=request.GET.get("claimant_id"))
        formset.fields["fund"].queryset = Fund.objects.filter(
            claimant=claimant,
            status__in=FUND_STATUS_APPROVED_SET
        )

    # Show submission form.
    context = {
        "title": "Edit blog post draft" if blog_to_edit else "Submit blog post draft",
        "formset": formset,
        "js_files": ["js/blog.js"],
    }
    return render(request, 'lowfat/form.html', context)


def blog_form_public(request, access_token):  # pylint: disable=too-many-branches
    try:
        fund = Fund.objects.get(access_token=access_token)
        if not fund.access_token_is_valid():
            fund = None
    except ObjectDoesNotExist:
        fund = None

    if fund is None:
        raise Http404("Funding request does not exist.")

    initial = {"fund": fund}

    formset = BlogForm(
        request.POST or None,
        request.FILES or None,
        initial=initial,
        is_staff=bool(request.user.is_staff)
    )

    if formset.is_valid():
        blog = formset.save()
        blog.author = blog.fund.claimant
        blog.new_access_token()
        blog.save()

        messages.success(request, 'Blog draft saved.')
        if not formset.cleaned_data["not_send_email_field"]:
            new_blog_notification(blog)
        return HttpResponseRedirect(
            reverse('blog_detail_public', args=[blog.access_token])
        )

    # Show submission form.
    context = {
        "title": "Submit blog post draft",
        "formset": formset,
        "js_files": ["js/blog.js"],
    }
    return render(request, 'lowfat/form.html', context)


def _blog_detail(request, blog):
    if blog is None:
        raise Http404("Blog doesn't exist.")

    context = {
        'blog': blog,
        'emails': BlogSentMail.objects.filter(blog=blog),
    }
    return render(request, 'lowfat/blog_detail.html', context)


@login_required
def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)

        if not (request.user.is_staff
                or Claimant.objects.get(user=request.user) == blog.author
                or Claimant.objects.get(user=request.user) in blog.coauthor.all()):
            blog = None

    except ObjectDoesNotExist:
        blog = None

    return _blog_detail(request, blog)


def blog_detail_public(request, access_token):
    try:
        blog = Blog.objects.get(access_token=access_token)
        if not blog.access_token_is_valid():
            blog = None
    except ObjectDoesNotExist:
        blog = None

    return _blog_detail(request, blog)


@login_required
def blog_edit(request, blog_id):
    if request.user.is_staff:  # pylint: disable=no-else-return
        return HttpResponseRedirect(
            reverse('admin:lowfat_blog_change', args=[blog_id])
        )
    else:
        return blog_form(request, blog_id=blog_id)


@staff_member_required
def blog_review(request, blog_id):
    this_blog = Blog.objects.get(id=blog_id)

    if request.POST:
        # Handle submission
        old_blog = copy.deepcopy(this_blog)
        formset = BlogReviewForm(request.POST, instance=this_blog)

        if formset.is_valid():
            blog = formset.save()
            messages.success(request, 'Blog updated.')
            if not formset.cleaned_data["not_send_email_field"]:
                blog_review_notification(
                    formset.cleaned_data['email'],
                    request.user,
                    old_blog,
                    blog,
                    not formset.cleaned_data['not_copy_email_field']
                )
            return HttpResponseRedirect(
                reverse('blog_detail', args=[blog.id])
            )

    formset = BlogReviewForm(
        None,
        instance=this_blog,
        is_staff=bool(request.user.is_staff)
    )

    # Limit dropdown list to staffs
    if not this_blog.reviewer:
        formset.fields["reviewer"].queryset = User.objects.filter(is_staff=True)

    context = {
        'blog': this_blog,
        'emails': BlogSentMail.objects.filter(blog=this_blog),
        'formset': formset,
    }

    return render(request, 'lowfat/blog_review.html', context)


@login_required
def blog_remove(request, blog_id):
    if request.user.is_staff:
        redirect_url = reverse('admin:lowfat_blog_delete', args=[blog_id])
    else:
        if "next" in request.GET:
            redirect_url = request.GET["next"]
        else:
            redirect_url = "/"

        try:
            this_blog = Blog.objects.get(id=blog_id)
        except:  # pylint: disable=bare-except
            this_blog = None
            messages.error(request, "The blog that you want to remove doesn't exist.")

        if this_blog and Claimant.objects.get(user=request.user) == this_blog.author:
            this_blog.remove()
            messages.success(request, 'Blog deleted with success.')
        else:
            messages.error(request, 'Only the author can remove the blog.')

    return HttpResponseRedirect(redirect_url)


@staff_member_required
def recent_actions(request):
    """Recent actions view."""
    action_list = []
    action_list.extend([(claimant.history_date, claimant) for claimant in Claimant.history.all()])  # pylint: disable=E1101
    action_list.extend([(fund.history_date, fund) for fund in Fund.history.all()])  # pylint: disable=E1101
    action_list.extend([(expense.history_date, expense) for expense in Expense.history.all()])  # pylint: disable=E1101
    action_list.extend([(blog.history_date, blog) for blog in Blog.history.all()])  # pylint: disable=E1101

    action_list.sort(key=lambda x: x[0], reverse=True)
    paginator = Paginator([action[1] for action in action_list], 10)

    page = request.GET.get('page')
    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        actions = paginator.page(1)
    except EmptyPage:
        actions = paginator.page(paginator.num_pages)

    context = {
        "actions": actions,
    }

    return render(request, "lowfat/recent_actions.html", context)


@staff_member_required
def report_by_name(request, report_filename):
    """Report view."""
    try:
        with open("lowfat/reports/html/{}".format(report_filename), "r") as _file:
            response = HttpResponse(_file.read(), content_type="text/plain")
            return response
    except:  # pylint: disable=bare-except
        raise Http404("Report does not exist.")  # pylint: disable=raise-missing-from


@staff_member_required
def report(request):
    """Report view."""
    context = {
        'notebook_filenames': [filename for filename in os.listdir("lowfat/reports/html/") if filename.endswith(".html")],
    }

    return render(request, 'lowfat/report.html', context)


@staff_member_required
def geojson(request):
    """Return the GeoJSON file."""

    context = {
        'claimants': Claimant.objects.all(),
        'funds': Fund.objects.all(),
    }

    return render(request, 'lowfat/map.geojson', context)
