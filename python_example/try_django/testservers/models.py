from django.db import models

# Create your models here.
TEST_SERVER_STATUS = (
    (-1, 'unknown'),
    (0, 'idle'),
    (1, 'busy'),
)

TEST_SERVER_TYPE = (
    (0, 'others'),
    (1, 'x86'),
    (2, 'kunpeng'),
    (3, 'ampere')
)


class TestServers(models.Model):

    mac_address = models.CharField(max_length=50, null=True, blank=True)
    hostname = models.CharField(max_length=100, default=None, null=True, blank=True)
    jenkins_node = models.CharField(max_length=50, default=None, null=True, blank=True)
    ip = models.GenericIPAddressField(protocol="ipv4", null=True, blank=True, default=None)
    ipmi = models.CharField(max_length=50, null=True, blank=True)
    server_os = models.CharField(max_length=20, null=True, blank=True)
    gpu_type = models.CharField(max_length=64, blank=True, null=True, default=None)
    server_type = models.IntegerField(default=0, choices=TEST_SERVER_TYPE)
    machine_info = models.CharField(max_length=1024, null=True, blank=True, default=None)
    location = models.CharField(max_length=20, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    usage = models.FloatField(null=True, blank=True, default=0)
    status = models.IntegerField(default=-1, choices=TEST_SERVER_STATUS)
