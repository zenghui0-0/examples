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
        fields = ['id', 'project_name', 'run_step', 'run_status', 'report_type', 'component', 'requester', 'requester_ip', 'test_end_time', 'create_time', 'passrate']
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
    phantomgv_data = serializers.SerializerMethodField()

    class Meta:
        model = TestReports
        fields = '__all__'

    def get_components(self, obj):
        if obj.components:
            return json.loads(obj.components.replace("'", "\""))

    def get_matrix_data(self, obj):
        objs_case = obj.test_case_run.all()
        other_case_list = objs_case.filter(testcase__type=0)
        other_failed_list = objs_case.filter(testcase__type=0, status__in=[3, 6])
        other_pass_list = objs_case.filter(testcase__type=0, status=2)
        userCase_case_list = objs_case.filter(testcase__type=1)
        userCase_failed_list = objs_case.filter(testcase__type=1, status__in=[3, 6])
        userCase_pass_list = objs_case.filter(testcase__type=1, status=2)
        reliability_case_list = objs_case.filter(testcase__type=2)
        reliability_failed_list = objs_case.filter(testcase__type=2, status__in=[3, 6])
        reliability_pass_list = objs_case.filter(testcase__type=2, status=2)
        robustness_case_list = objs_case.filter(testcase__type=3)
        robustness_failed_list = objs_case.filter(testcase__type=3, status__in=[3, 6])
        robustness_pass_list = objs_case.filter(testcase__type=3, status=2)
        performance_case_list = objs_case.filter(testcase__type=4)
        performance_failed_list = objs_case.filter(testcase__type=4, status__in=[3, 6])
        performance_pass_list = objs_case.filter(testcase__type=4, status=2)
        power_case_list = objs_case.filter(testcase__type=5)
        power_failed_list = objs_case.filter(testcase__type=5, status__in=[3, 6])
        power_pass_list = objs_case.filter(testcase__type=5, status=2)
        matrix_data = {"Others": {"All": len(other_case_list), "Failed": len(other_failed_list), "Pass": len(other_pass_list)},
                       "UseCases": {"All": len(userCase_case_list), "Failed": len(userCase_failed_list), "Pass": len(userCase_pass_list)},
                       "Reliability": {"All": len(reliability_case_list), "Failed": len(reliability_failed_list), "Pass": len(reliability_pass_list)},
                       "Robustness": {"All": len(robustness_case_list), "Failed": len(robustness_failed_list), "Pass": len(robustness_pass_list)},
                       "Performance": {"All": len(performance_case_list), "Failed": len(performance_failed_list), "Pass": len(performance_pass_list)},
                       "Power": {"All": len(power_case_list), "Failed": len(power_failed_list), "Pass": len(power_pass_list)}}
        new_matrix_data = {"AllTestDone":True}
        return matrix_data
