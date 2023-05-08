from rest_framework import serializers
from users.serializer import UserSerializer
from testservers.serializer import TestServerSerializer
from .models import *
from testservers.models import TestServers
import json


class TestCaseRunSerializer(serializers.ModelSerializer):
    test_server = TestServerSerializer(read_only=True)

    class Meta:
        model = TestCaseRun
        fields = '__all__'


class TestReportsSerializer(serializers.ModelSerializer):
    passrate = serializers.SerializerMethodField()

    class Meta:
        model = TestReports
        fields = ['id', 'project_name', 'run_step', 'run_status',
                  'report_type', 'component', 'test_report_url',
                  'artifactory_url', 'comment', 'requester',
                  'requester_ip', 'test_end_time', 'create_time', 'passrate']
        ordering = ['-create_time']

    def get_passrate(self, obj):
        if obj.test_case_run.all().count() > 0:
            return int(len([item for item in obj.test_case_run.all() if item.status == 2]) / obj.test_case_run.all().count() * 100)
        else:
            return ''


class TestReportDetailSerializer(TestReportsSerializer):
    test_case_run = TestCaseRunSerializer(read_only=True, many=True)
    matrix_data = serializers.SerializerMethodField()
    components = serializers.SerializerMethodField()

    class Meta:
        model = TestReports
        fields = '__all__'

    def get_components(self, obj):
        # Todo: this should turn to dictionary
        return obj.test_case_run.all()

    def get_matrix_data(self, obj):
        new_matrix_data = {"AllTestDone":True}
        return new_matrix_data
