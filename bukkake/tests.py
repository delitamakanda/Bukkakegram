import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCaseMixin
from bukkake.models import Bukkake

# Create your tests here.

class BukkakeResourceTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super(BukkakeResourceTest, self).setUp()

        self.username = 'root'
        self.password = 'root'
        self.user = User.objects.create_user(self.username, 'root@example.com', self.password)
        self.bukkake_1 = Bukkake.objects.get(slug='bukkake-one')
        self.detail_url = '/api/v1/bukkake/{0}'.format(self.bukkake_1.pk)
        self.post_data = {
            'user': '/api/v1/user/{0}/'.format(self.user.pk),
            'title': 'Bukkake',
            'slug': 'bukkake-one',
            'description': 'bukkake test case',
            'url': '',
            'image': '',
            'created': '2012-05-01T22:05:12'
        }

    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)
