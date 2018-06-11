from django.test import TestCase
from .models import Topic
from django.utils import timezone

# Create your tests here.
t = Topic(name="Ala ma kota", timestamp=timezone.now())
t.save()
