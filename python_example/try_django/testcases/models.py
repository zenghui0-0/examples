from django.db import models

# Create your models here.
TEST_CASE_TYPE = (
    (0, 'Other'),
)

class TestCases(models.Model):

    name = models.CharField(max_length=255)
    caseid = models.IntegerField(default=0)
    case_type = models.IntegerField(default=0, choices=TEST_CASE_TYPE)
    feature = models.CharField(max_length=255, default=None, null=True, blank=True)
    runtime = models.CharField(max_length=10, null=True, blank=True)
    timeout = models.CharField(max_length=10, null=True, blank=True)
    description = models.CharField(max_length=5000, default=None, null=True)
    comment = models.CharField(max_length=255, default=None, null=True, blank=True)
    active = models.BooleanField(default=True)

