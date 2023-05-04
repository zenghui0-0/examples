from rest_framework import serializers
from .models import *


class TestReportSimpleSerializer(serializers.ModelSerializer):
    passrate = serializers.SerializerMethodField()

    class Meta:
        model = TestReports
        fields = ['id', 'project_name', 'run_step', 'run_status', 'report_type', 'component', 'requester', 'requester_ip', 'create_time', 'passrate']
        ordering = ['-create_time']

    def get_passrate(self, obj):
        if obj.test_case_run.all().count() > 0:
            return int(len([item for item in obj.test_case_run.all() if item.status == 2]) / obj.test_case_run.all().count() * 100)
        else:
            return ''
