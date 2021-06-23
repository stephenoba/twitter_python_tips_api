import collections

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


def AVAILABLE_APIS(request, format):  # noqa
    return [
        ("twitter_login", reverse("twitter-login", request=request, format=format)),
        ("rest_logout", reverse("rest_logout", request=request, format=format)),
        ("tips", reverse("tip-list", request=request, format=format)),
        ("entry_list", reverse("entry-list", request=request, format=format)),
    ]


@api_view(("GET",))
def api_root(request, format=None):
    """
    GET:
    Display all available urls.
    """
    apis = AVAILABLE_APIS(request, format)

    return Response(collections.OrderedDict(apis))
