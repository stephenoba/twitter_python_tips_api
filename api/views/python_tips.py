from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView, ListCreateAPIView,
)
from rest_framework import permissions

from python_tips.models import Tip, Entry
from ..serializers.python_tips import TipSerializer, EntrySerializer


class TipListAPIView(ListAPIView):
    queryset = Tip.objects.all()
    serializer_class = TipSerializer


class TipRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Tip.objects.all()
    serializer_class = TipSerializer
    permission_classes = (permissions.IsAdminUser,)


class EntryListAPIView(ListCreateAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = (permissions.IsAuthenticated,)
