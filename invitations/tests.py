import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Question

class AppUser(TestCase):
    def setUp(self):
        #Setup run before every test method.
        pass

    def tearDown(self):
        #Clean up run after every test method.
        pass

    def appuser_exists(self):
        pass

class Event(TestCase):
    def setUp(self):
        #Setup run before every test method.
        pass

    def tearDown(self):
        #Clean up run after every test method.
        pass

    def event_exists(self):
        pass

class Rsvp(TestCase):
    def setUp(self):
        #Setup run before every test method.
        pass

    def tearDown(self):
        #Clean up run after every test method.
        pass

    def rsvp_exists(self):
        pass
