from django.db import models
from users.models import Users
from testservers.models import TestServers


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

TEST_CASE_RUN_TYPE = (
    (0, 'testrun'),
    (1, 'prepare'),
    (2, 'post'),
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
    testcase_run_type = models.IntegerField(default=0, choices=TEST_CASE_RUN_TYPE)
    comment = models.CharField(max_length=1024, null=True, blank=True, default=None)
    test_server = models.ForeignKey(TestServers, related_name='testcase_run', on_delete=models.DO_NOTHING, default=None, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class ReportComponent(models.Model):

    component_name = models.CharField(max_length=50, null=True, blank=True)
    component_value = models.CharField(max_length=100, null=True, blank=True)


class TestReports(models.Model):

    project_name = models.CharField(max_length=50, null=True, blank=True)
    test_case_run = models.ManyToManyField(TestCaseRun, related_name='testreports', default=None)
    run_step = models.IntegerField(default=0, choices=TEST_REPORT_RUN_STEP) # step
    run_status = models.BooleanField(default=True) # True: running, False: finished
    report_type = models.IntegerField(default=0, choices=TEST_REPORT_TYPE)
    component = models.ManyToManyField(ReportComponent, related_name='testreports', default=None)
    comment = models.CharField(max_length=1024, null=True, blank=True, default=None)
    requester = models.CharField(max_length=50, null=True, blank=True, default=None)
    requester_ip = models.CharField(max_length=50, null=True, blank=True, default=None)
    test_end_time = models.DateTimeField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

class TestServerRecord(models.Model):
    testserver = models.ForeignKey(TestServers, related_name='testserver_record', null=True, on_delete=models.SET_NULL)
    testreports = models.ForeignKey(TestReports, related_name='testserver_record', on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
