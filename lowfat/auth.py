"""
Funtions used on Python Social Auth Pipeline.

More details about pipeline
at http://python-social-auth.readthedocs.io/en/latest/pipeline.html
"""
from .models import Claimant


def wire_profile(backend, user, response, details, *args, **kwargs):  #pylint: disable=unused-argument

    """Wire GitHub profile with Fellow profile.

    :param backend: Backend from Python Social Auth. Must be <social_core.backends.github.GithubOAuth2 object at 0x7f9a97b1a198>
    :param user: The Django user instance
    :param response: The server user-details response. E.g.

    {'bio': None, 'public_gists': 2, 'access_token': 'token', 'gists_url': 'https://api.github.com/users/foo/gists{/gist_id}', 'html_url': 'https://github.com/foo', 'email': 'foo@mail.com', 'events_url': 'https://api.github.com/users/foo/events{/privacy}', 'id': 1506457, 'type': 'User', 'following': 39, 'starred_url': 'https://api.github.com/users/foo/starred{/owner}{/repo}', 'url': 'https://api.github.com/users/foo', 'updated_at': '2017-02-21T15:49:59Z', 'scope': '', 'hireable': None, 'avatar_url': 'https://avatars.githubusercontent.com/u/xxxxxxx?v=3', 'name': 'Foo Bar', 'location': None, 'gravatar_id': '', 'token_type': 'bearer', 'received_events_url': 'https://api.github.com/users/foo/received_events', 'organizations_url': 'https://api.github.com/users/foo/orgs', 'public_repos': 144, 'site_admin': False, 'blog': None, 'company': None, 'created_at': '2012-03-06T10:27:54Z', 'following_url': 'https://api.github.com/users/foo/following{/other_user}', 'followers': 57, 'subscriptions_url': 'https://api.github.com/users/foo/subscriptions', 'repos_url': 'https://api.github.com/users/foo/repos', 'followers_url': 'https://api.github.com/users/foo/followers', 'login': 'foo'}

    :param details: Basic user details generated by the backend. E.g.

    {'email': 'foo@mail.com', 'first_name': 'Foo', 'fullname': 'Foo Bar', 'username': 'foo', 'last_name': 'Bar'}

    :returns: None
    :rtype: None
    """
    if backend.name == 'github':
        # FIXME Need to include collaborator=True
        claimant = Claimant.objects.filter(
            github=response["login"],
            fellow=True
        ).order_by(
            "application_year"
        ).reverse()
        if claimant:
            claimant[0].user = user
            claimant[0].save()
