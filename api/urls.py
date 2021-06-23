from django.urls import path
from django.conf.urls import url

from .views.python_tips import TipListAPIView, TipRetrieveAPIView, EntryListAPIView
from .views.login import TwitterLogin
from .views.root import api_root

urlpatterns = [
    path("", api_root, name="api-root"),
    path("tips/", TipListAPIView.as_view(), name="tip-list"),
    path("tips/<int:pk>/", TipRetrieveAPIView.as_view(), name="tip-detail"),
    path("entries/", EntryListAPIView.as_view(), name="entry-list"),
    url('auth/twitter/$', TwitterLogin.as_view(), name='twitter-login'),
]
