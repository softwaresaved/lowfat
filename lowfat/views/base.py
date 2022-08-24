import pathlib
import typing

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, Http404
from django.views.generic import DetailView

import magic

PathLike = typing.Union[str, pathlib.Path]


def deprecated_view(request, *args, **kwargs):
    raise Http404("URL not supported in lowFAT 2.x.")


class FileFieldView(DetailView):
    """View to download the contents of a FileField."""
    field_name: str

    @staticmethod
    def clean_name(name: PathLike) -> str:
        return str(name).replace("/", "-")

    def render_to_response(self, context, **response_kwargs):
        field = getattr(self.object, self.field_name)

        try:
            with open(field.path, "rb") as _file:
                content = _file.read()

                mime_type = magic.from_buffer(content, mime=True)
                response = HttpResponse(content, content_type=mime_type)

                clean_name = self.clean_name(field.name)
                response[
                    'Content-Disposition'] = f'inline; filename="{clean_name}"'

        except ValueError as exc:
            raise Http404("File not found") from exc

        return response


class OwnerStaffOrTokenMixin(UserPassesTestMixin):
    """Allow access only to the owner of an object, to staff, or with a token."""
    #: Allow bypassing user account check with a token
    allow_token: bool = True

    #: Field representing the owner of the checked object
    owner_field: str

    @staticmethod
    def recurse_getattr(obj, attr_string: str):
        for attr in attr_string.split("."):
            obj = getattr(obj, attr)

        return obj

    def test_func(self) -> bool:
        obj = self.get_object()

        if self.allow_token and "token" in self.kwargs:
            return obj.access_token_is_valid()

        return self.request.user.is_staff or self.request.user == self.recurse_getattr(
            obj, self.owner_field)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise Http404

        return super().handle_no_permission()
