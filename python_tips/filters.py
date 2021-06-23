from django import forms
import django_filters

from python_tips.models import Tip


class TipFilterSet(django_filters.FilterSet):
    full_text = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Enter search term',
        'class': 'form-control-sm mr-sm-2',
    }))

    o = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('num_retweets', 'retweets'),
            ('num_likes', 'likes'),
        ),
    )

    class Meta:
        model = Tip
        fields = ('full_text',)
