from django.db import models
from users.models import Users


# Create your models here.
TEST_REPORT_RUN_STEP = (
    (0, 'others'),
    (1, 'Prepare'),
    (2, 'Install'),
    (3, 'Testing'),
    (4, 'Finished'),
    (5, 'Aborted'),
    (6, 'Promoted'),
    (7, 'Blocked')
)

TEST_CASE_RUN_STATUS = (
    (0, 'waiting'),
    (1, 'running'),
    (2, 'pass'),
    (3, 'failed'),
    (4, 'abort'),
    (5, 'timeout'),
    (6, 'regression'),
)

TEST_REPORT_TYPE = (
    (0, 'others'),
    (1, 'pre-submission'),
    (2, 'daily'),
    (3, 'weekly'),
    (4, 'release'),
)

class TestCaseRun(models.Model):

    testcase_name = models.CharField(max_length=50, null=True, blank=True)
    status = models.IntegerField(default=0, choices=TEST_CASE_RUN_STATUS)
    result = models.CharField(max_length=64, blank=True, null=True, default=None)
    comment = models.CharField(max_length=1024, null=True, blank=True, default=None)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class TestReports(models.Model):

    project_name = models.CharField(max_length=50, null=True, blank=True)
    test_case_run = models.ManyToManyField(TestCaseRun, related_name='testreports', default=None)
    run_step = models.IntegerField(default=0, choices=TEST_REPORT_RUN_STEP) # step
    run_status = models.BooleanField(default=True) # True: running, False: finished
    report_type = models.IntegerField(default=0, choices=TEST_REPORT_TYPE)
    comment = models.CharField(max_length=1024, null=True, blank=True, default=None)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


"""
class TestServer(models.Model):

    mac_address = models.CharField(max_length=50, null=True, blank=True)
    hostname = models.CharField(max_length=100, default=None, null=True, blank=True)
    jenkins_node = models.CharField(max_length=50, default=None, null=True, blank=True)
    ip = models.CharField(max_length=100, null=True, blank=True, default=None)
    ipmi = models.CharField(max_length=50, null=True, blank=True)
    type = models.IntegerField(default=0, choices=TEST_SERVER_TYPE)
    machine_info = models.CharField(max_length=1024, null=True, blank=True, default=None)
    location = models.CharField(max_length=20, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    usage = models.FloatField(null=True, blank=True, default=0)
    status = models.IntegerField(default=-1, choices=TEST_SERVER_STATUS)
"""
