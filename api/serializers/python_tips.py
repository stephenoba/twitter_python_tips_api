import requests
from fuzzywuzzy.process import extractOne

from django.conf import settings
from rest_framework import serializers

from python_tips.models import Tip, Link, Entry
from core.exceptions import GoogleFormError, SimilarEntryException


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = "__all__"


class TipSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="tip-detail")
    links = LinkSerializer(many=True)

    class Meta:
        model = Tip
        fields = ("url", "id", "tweet_id", "full_text", "num_likes",
                  "num_retweets", "links")


class EntrySerializer(serializers.ModelSerializer):
    python_tip = serializers.CharField(max_length=140)

    URL = settings.GOOGLE_FORM_URL
    FIELDS = settings.GOOGLE_FORM_FIELDS

    class Meta:
        model = Entry
        fields = ("id", "user", "python_tip", "twitter_id", "email", "published")
        read_only_fields = ("published", "twitter_id", "email")

    def validate(self, attrs):
        python_tip = attrs.get("python_tip")
        entries = Entry.objects.all()
        entry_tips = list(map(lambda x: x.python_tip, entries))
        # validate that python tip entry is not similar with other
        # entries or is not a repeated entry we use fuzzywuzzy which
        # implements the Levenshtien distance
        _, dis = extractOne(python_tip, entry_tips)
        # if the distance is above 95% then there is a high chance this is
        # a repeated tip.
        if dis >= 95:
            raise SimilarEntryException("Python tip already has a similar entry")
        return super(EntrySerializer, self).validate(attrs)

    def create(self, validated_data):
        python_tip = validated_data.get("python_tip")
        twitter_id = validated_data.get("twitter_id", "")
        email = validated_data.get("email", "")
        user = validated_data["user"]

        data = {
            self.FIELDS.get("python_tip"): python_tip,
            self.FIELDS.get("twitter_id"): twitter_id,
            self.FIELDS.get("email"): email
        }

        status_code = self.send_response(data)
        if not status_code == 200:
            raise GoogleFormError("Error with google form")
        validated_data["twitter_id"] = user.twitter_id
        validated_data["email"] = user.email
        return super(EntrySerializer, self).create(validated_data)

    def send_response(self, data):
        """
        sends response to google form
        """
        if not self.URL:
            raise GoogleFormError("No url provided")
        res = requests.post(self.URL, data=data)
        status_code = res.status_code
        return status_code
