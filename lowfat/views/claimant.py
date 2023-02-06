from datetime import datetime
import logging
import sys
import zipfile

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from constance import config

from lowfat.forms import ClaimantForm, FellowForm
from lowfat.mail import claimant_profile_update_notification
from lowfat.models import Blog, Claimant, Expense, Fund, FUND_STATUS_APPROVED_SET, TermsAndConditions, pair_fund_with_blog

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def get_terms_and_conditions_url(request):
    """Return the terms and conditions link associated with the user."""
    try:
        url = TermsAndConditions.objects.get(
            year=str(timezone.now().year)
        ).url

    except TermsAndConditions.DoesNotExist as exc:
        message = "Could not find terms and conditions URL for this year"
        messages.error(request, message)
        logger.error(message)
        raise Http404(message) from exc

    if not request.user.is_staff:
        try:
            claimant = Claimant.objects.get(user=request.user)
            url = claimant.terms_and_conditions.url

        except (AttributeError, TypeError):
            # Claimant has no terms and conditions linked or is Anonymous user
            # Use this years T&Cs as default and log a warning

            messages.warning(
                request,
                'You do not have a specific terms and conditions linked to your profile. '
                'Please contact an admin to resolve this. '
                'As a default, we are now using this year\'s terms and conditions.'
            )
            logger.warning('No terms and conditions for user %s, using default for this year')

            try:
                url = TermsAndConditions.objects.get(
                    year=str(timezone.now().year)
                ).url

            except TermsAndConditions.DoesNotExist as exc:
                message = "Could not find terms and conditions URL for this year"
                messages.error(request, message)
                logger.error(message)
                raise Http404(message) from exc

        except Claimant.DoesNotExist as exc:
            raise Http404('Claimant does not exist') from exc

        except Claimant.MultipleObjectsReturned as exc:
            message = 'Multiple claimants exist with the same registered user. ' \
                      'Please contact an admin to fix this.'

            messages.error(request, message)
            logger.error(message)
            raise Http404(message) from exc

    return url


def index(request):
    context = {
        'claimants': Claimant.objects.filter(
            Q(fellow=True) | Q(collaborator=True)
        ),
        'funds': [(fund, Blog.objects.filter(
            fund=fund,
            status="P"
        )) for fund in Fund.objects.filter(category="H", start_date__gte=timezone.now(), can_be_advertise_before=True)],
    }

    return render(request, 'lowfat/index.html', context)

def event_report(request):
    
    current_year = datetime.now().year
    
    funds = Fund.objects.filter(
            status__in = {"A", "M", "F"},
            mandatory = False,
            start_date__year = current_year,
    ) 
    
    n_funds = len(funds)
    
    domain_specific_events_attended = funds.filter(
            focus = "D",
            category = "A"
    )
    
    n_domain_specific_events_attended = len(domain_specific_events_attended)
    
    domain_specific_events_organised = funds.filter(
            focus = "D",
            category = "H",
        )
    
    n_domain_specific_events_organised = len(domain_specific_events_organised)
    
    cross_cutting_events_attended = funds.filter(
            focus = "C",
            category = "A",
        )

    n_cross_cutting_events_attended = len(cross_cutting_events_attended)
    
    cross_cutting_events_organised = funds.filter(
            focus = "C",
            category = "H",
        )
    
    n_cross_cutting_events_organised = len(cross_cutting_events_organised)

    context = {
        'current_year': current_year,
        'funds': funds,
        'n_funds': n_funds,
        'domain_specific_events_attended': domain_specific_events_attended, 
        'n_domain_specific_events_attended': n_domain_specific_events_attended,
        'domain_specific_events_organised': domain_specific_events_organised,
        'n_domain_specific_events_organised': n_domain_specific_events_organised,
        'cross_cutting_events_attended': cross_cutting_events_attended,
        'n_cross_cutting_events_attended': n_cross_cutting_events_attended,
        'cross_cutting_events_organised': cross_cutting_events_organised, 
        'n_cross_cutting_events_organised': n_cross_cutting_events_organised,             
    }
    return render(request, 'lowfat/event_report.html', context)


@login_required
def dashboard(request):
    context = {
        'ical_token': config.CALENDAR_ACCESS_TOKEN,
    }

    if not request.user.is_staff:
        try:
            claimant = Claimant.objects.get(user=request.user)

        except Claimant.DoesNotExist:
            logger.warning('No claimant found for user %s', request.user.username)
            return HttpResponseRedirect(reverse('django.contrib.flatpages.views.flatpage', kwargs={'url': '/welcome/'}))

        # Setup query parameters
        funding_requests_status = request.GET["funding_requests"] if "funding_requests" in request.GET else "UPAMRF"  # Pending
        expenses_status = request.GET["expenses"] if "expenses" in request.GET else "WSCPAF"  # All
        blogs_status = request.GET["blogs"] if "blogs" in request.GET else "URCGLPMDOX"  # All

        context.update(
            {
                'funding_requests_status': funding_requests_status,
                'expenses_status': expenses_status,
                'blogs_status': blogs_status,
                'claimant': claimant,
                'budget_available': claimant.claimantship_available(),
                'funds': pair_fund_with_blog(
                    Fund.objects.filter(
                        claimant=claimant,
                        status__in=funding_requests_status
                    ),
                    "P"
                ),
                'expenses': Expense.objects.filter(
                    fund__claimant=claimant,
                    status__in=expenses_status
                ),
                'blogs': Blog.objects.filter(
                    Q(author=claimant, status__in=blogs_status) | Q(coauthor=claimant, status__in=blogs_status)
                    # Need to get distinct otherwise posts will be shown twice if user is author and coauthor
                    # This happens here because the two ORed filter components operate on different table joins
                ).distinct(),
            }
        )
    else:
        # Setup query parameters
        funding_requests_status = request.GET["funding_requests"] if "funding_requests" in request.GET else "UP"  # Pending
        expenses_status = request.GET["expenses"] if "expenses" in request.GET else "WSCP"  # Pending
        blogs_status = request.GET["blogs"] if "blogs" in request.GET else "URCGL"  # Pending

        context.update(
            {
                'funding_requests_status': funding_requests_status,
                'expenses_status': expenses_status,
                'blogs_status': blogs_status,
                'funds': pair_fund_with_blog(
                    Fund.objects.filter(
                        status__in=funding_requests_status
                    ),
                    "P"
                ),
                'expenses': Expense.objects.filter(
                    status__in=expenses_status
                ),
                'blogs': Blog.objects.filter(
                    status__in=blogs_status
                ),
            }
        )

    return render(request, 'lowfat/dashboard.html', context)


@staff_member_required
def staff(request):
    context = {}
    return render(request, 'lowfat/staff.html', context)


@staff_member_required
def get_fellows_photos(request):
    zip_filename = "/tmp/fellows_photos{}.zip".format(
        datetime.now().isoformat(timespec='minutes')
    )

    with zipfile.ZipFile(zip_filename, "w") as fellows_photos_zip:
        for fellow in Claimant.objects.filter(fellow=True):
            fellows_photos_zip.write(
                fellow.photo.path,
                "{}.jpg".format(fellow.slug)
            )

    return HttpResponse(
        open(zip_filename, 'rb'),
        content_type='application/zip'
    )


@staff_member_required
def rss(request):
    context = {
        'claimants': Claimant.objects.filter(fellow=True),
    }
    return render(request, 'lowfat/rss.opml', context)


@staff_member_required
def search(request):
    search_text = request.POST.get("search")
    context = {
        "search": search_text,
        "fellows": Claimant.objects.filter(
            (
                Q(forenames__contains=search_text)
                | Q(surname__contains=search_text)
                | Q(email__contains=search_text)
                | Q(research_area__contains=search_text)
                | Q(affiliation__contains=search_text)
                | Q(work_description__contains=search_text)
                | Q(website__contains=search_text)
                | Q(github__contains=search_text)
                | Q(twitter__contains=search_text)
            ) & (Q(fellow=True) | Q(collaborator=True))
        ),
        "claimants": Claimant.objects.filter(
            (
                Q(forenames__contains=search_text)
                | Q(surname__contains=search_text)
                | Q(email__contains=search_text)
                | Q(research_area__contains=search_text)
                | Q(affiliation__contains=search_text)
                | Q(work_description__contains=search_text)
                | Q(website__contains=search_text)
                | Q(github__contains=search_text)
                | Q(twitter__contains=search_text)
            ) & Q(fellow=False)
        ),
        "funds": Fund.objects.filter(
            Q(claimant__forenames__contains=search_text)
            | Q(claimant__surname__contains=search_text)
            | Q(title__contains=search_text)
            | Q(url__contains=search_text)
            | Q(justification__contains=search_text)
            | Q(additional_info__contains=search_text)
        ),
    }

    return render(request, 'lowfat/search.html', context)


@staff_member_required
def promote(request):
    context = {
        "claimants": Claimant.objects.filter(),
    }

    return render(request, 'lowfat/promote.html', context)


@login_required
def claimant_form(request):
    if not request.user.is_staff:
        instance = Claimant.objects.get(user=request.user)
        title_begin = "Edit"
    else:
        instance = None
        title_begin = "Create"

    if "full" in request.GET:
        formset = FellowForm(request.POST or None, request.FILES or None, instance=instance)
        title_end = "fellow"
    else:
        formset = ClaimantForm(request.POST or None, request.FILES or None, instance=instance)
        title_end = "claimant"

    if formset.is_valid():
        claimant = formset.save()
        claimant.update_latlon()
        messages.success(request, 'Profile saved.')
        claimant_profile_update_notification(claimant)
        return HttpResponseRedirect(
            reverse('claimant_slug', args=[claimant.slug])
        )

    # Show submission form.
    context = {
        "title": "{} {}".format(title_begin, title_end),
        "formset": formset,
        "submit_text": "Save" if instance is None else "Update",
    }
    return render(request, 'lowfat/form.html', context)


@staff_member_required  # pylint: disable=unused-argument
def claimant_promote(request, claimant_id):
    claimant = Claimant.objects.get(id=claimant_id)
    claimant.fellow = True
    claimant.save()
    messages.success(
        request,
        '{} promoted to Fellow.'.format(claimant.fullname())
    )

    return HttpResponseRedirect(
        reverse('fellow_slug', args=[claimant.slug])
    )


@staff_member_required
def claimant_demote(request, claimant_id):
    claimant = Claimant.objects.get(id=claimant_id)
    claimant.fellow = False
    claimant.save()
    messages.success(
        request,
        '{} is NOT a Fellow anymore.'.format(claimant.fullname())
    )

    return HttpResponseRedirect(
        reverse('fellow_slug', args=[claimant.slug])
    )


def _claimant_detail(request, claimant):
    """Details about claimant."""
    # Avoid leak information from applicants
    if request.user.is_staff:
        pass
    elif claimant.fellow or claimant.collaborator:
        pass
    elif claimant.received_offer and (claimant.user == request.user):
        pass
    else:
        raise Http404("Claimant does not exist.")

    # Setup query parameters
    funding_requests_status = request.GET["funding_requests"] if "funding_requests" in request.GET else "UPAMRF"
    expenses_status = request.GET["expenses"] if "expenses" in request.GET else "WSCPAF"
    blogs_status = request.GET["blogs"] if "blogs" in request.GET else "URGLPDO"

    context = {
        'funding_requests_status': funding_requests_status,
        'expenses_status': expenses_status,
        'blogs_status': blogs_status,
        'claimant': claimant,
    }

    if request.user.is_staff:
        funds = Fund.objects.filter(
            claimant=claimant,
            status__in=funding_requests_status
        )
        context.update(
            {
                'funds': pair_fund_with_blog(funds, "P"),
                'expenses': Expense.objects.filter(
                    fund__claimant=claimant,
                    status__in=expenses_status
                ),
                'blogs': Blog.objects.filter(
                    Q(author=claimant, status__in=blogs_status) | Q(coauthor=claimant, status__in=blogs_status)
                    # Distinct is required here - see comment in dashboard view
                ).distinct(),
            }
        )
    else:
        funds = Fund.objects.filter(
            claimant=claimant,
            can_be_advertise_after=True,
            status__in=FUND_STATUS_APPROVED_SET
        )
        context.update(
            {
                'funds': pair_fund_with_blog(funds, "P"),
                'blogs': Blog.objects.filter(
                    Q(author=claimant, status="P") | Q(coauthor=claimant, status="P")
                    # Distinct is required here - see comment in dashboard view
                ).distinct(),
            }
        )

    return render(request, 'lowfat/claimant_detail.html', context)


def claimant_detail(request, claimant_id):
    raise Http404("URL not supported in lowFAT 2.x.")


def claimant_slug_resolution(request, claimant_slug):
    """
    Resolve claimant slug and return the details.
    """
    try:
        claimant = Claimant.objects.get(slug=claimant_slug)
        return _claimant_detail(request, claimant)

    except Claimant.DoesNotExist as exc:
        raise Http404('Claimant does not exist') from exc

    except Claimant.MultipleObjectsReturned as exc:
        message = 'Multiple claimants exist with the same slug identifier "{0}". ' \
                  'Please contact an admin to fix this.'.format(claimant_slug)

        messages.error(request, message)
        logger.error(message)
        raise Http404(message) from exc


@login_required
def my_profile(request):
    if not request.user.is_staff:
        try:
            claimant = Claimant.objects.get(user=request.user)

        except:
            logger.warning('Exception caught by bare except')
            logger.warning('%s %s', *(sys.exc_info()[0:2]))

            return HttpResponseRedirect(reverse('django.contrib.flatpages.views.flatpage', kwargs={'url': '/unavailable/'}))

        return _claimant_detail(request, claimant)

    raise Http404("Claimant does not exist.")
