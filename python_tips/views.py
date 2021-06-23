from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from python_tips.models import Tip
from python_tips.filters import TipFilterSet


def index_view(request):
    tips_qs = Tip.objects.all()
    filters = TipFilterSet(request.GET, queryset=tips_qs)
    page_size = 10
    # get full_text and ordering from request to maintain the queryset
    # when a user changes the page.
    full_text = request.GET.get("full_text", "")
    ordering = request.GET.get("o", "")

    paginator = Paginator(filters.qs, page_size)
    try:
        tips = paginator.page(request.GET.get("page"))
    except PageNotAnInteger:
        tips = paginator.page(1)
    except EmptyPage:
        tips = paginator.page(paginator.num_pages)

    context = {
        'request': request,
        'tips': tips,
        'filters': filters,
        'full_text': full_text,
        'ordering': ordering,
        "is_paginated": True
    }

    return render(request, 'python_tips/index.html', context)
