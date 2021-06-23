from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.utils import timezone
from rest_framework import status
from rest_framework.test import force_authenticate

from users.models import User
from python_tips.models import Tip, Entry
from ..serializers.python_tips import TipSerializer, EntrySerializer
from ..views.python_tips import EntryListAPIView

client = Client()
factory = RequestFactory()


class GetTipTest(TestCase):

    def setUp(self):
        self.first_tip = Tip.objects.create(
            tweet_id=12345678912345,
            full_text='Probability Distribution Explorer '
                      'is a tool to explore commonly used probability '
                      'distributions with syntax on how to use these '
                      'distributions in #NumPy, #SciPy, and #Stan.\n\n<'
                      'see link below> <see link below>',
            num_retweets=156,
            num_likes=320,
            timestamp=timezone.now()
        )
        self.second_tip = Tip.objects.create(
            tweet_id=12345664912345,
            full_text='Python offers several solutions for short-term storage\n'
                      '* pickle.dump(obj,f)   # Save an object obj into a file f\n'
                      '* dill: able to pickle more data types\n* shelve: to save '
                      'dict of objects <see link below>\n* diskcache: faster, safer, '
                      'Django integration <see link below>',
            num_retweets=56,
            num_likes=190,
            timestamp=timezone.now()
        )

    def test_get_valid_tips(self):
        response = client.get('/api/tips/')
        tips = Tip.objects.all()
        serializer = TipSerializer(tips, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EntryRequestTest(TestCase):

    def setUp(self):
        tip = """Probability Distribution Explorer is a tool to explore commonly used probability 
                distributions with syntax on how to use these
                distributions in #NumPy, #SciPy, and #Stan.\n\n<
                see link below> <see link below>"""
        self.user = User.objects.create_user(email="test@example.com", password="767&&00 IUJ")
        self.first_entry = Entry.objects.create(
            user=self.user,
            python_tip=tip,
            twitter_id=self.user.twitter_id,
            email=self.user.email,
        )
        self.second_entry = Entry.objects.create(
            user=self.user,
            python_tip='Python offers several solutions for short-term storage\n'
                       '* pickle.dump(obj,f)   # Save an object obj into a file f\n'
                       '* dill: able to pickle more data types\n* shelve: to save '
                       'dict of objects <see link below>\n* diskcache: faster, safer, '
                       'Django integration <see link below>',
            twitter_id=self.user.twitter_id,
            email=self.user.email,
        )
        self.invalid_data = {
            "user": self.user.id,
            "python_tip": tip,
            "twitter_id": self.user.twitter_id,
            "email": self.user.email
        }
        self.valid_data = {
            "user": self.user.id,
            "python_tip": 'Looking for quick-and-dirty #docs for your Python project? '
                          'pycco):\n<see link below>\n\nMore detailed intro:\n<see link below>',
            "twitter_id": self.user.twitter_id,
            "email": self.user.email
        }

    def test_get_valid_entries(self):
        entries = Entry.objects.all()
        view = EntryListAPIView.as_view()
        request = factory.get('/api/entries/')
        force_authenticate(request, user=self.user)
        response = view(request)
        serializer = EntrySerializer(entries, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_invalid_entries(self):
        view = EntryListAPIView.as_view()
        request = factory.post('/api/entries/', data=self.invalid_data)
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_valid_entries(self):
        view = EntryListAPIView.as_view()
        request = factory.post('/api/entries/', data=self.valid_data)
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
