from django.shortcuts import render
from rest_framework import viewsets
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializer import TestReportsSerializer, ReportComponentSerializer, TestReportDetailSerializer, TestCaseRunSerializer
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt
from utils.tools import MyPage, page_paginator, get_parameter_dic
from .models import TestReports, TestCaseRun, ReportComponent
from testservers.models import TestServers
from users.models import Users
import datetime
import json


# Create your views here.
class TestReportsView(viewsets.ModelViewSet):
    queryset = TestReports.objects.all()
    serializer_class = TestReportsSerializer
    pagination_class = MyPage # ??
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter] # ??
    filterset_fields = ('id', 'project_name', 'report_type') # django_filters
    search_fields = ('id', 'project_name', 'report_type') # ??
    ordering_fields = ('id', 'create_time') # ??
    ordering = ['-create_time'] # ??

    """
    def list_(self, request, *args, **kwargs):
        params = get_parameter_dic(request)
        print(f"in list params is: {params}")
        queryset = Q()
        report_id = params.get('id', None)
        if report_id is not None:
            queryset &= Q(id=report_id)
        if params.get("project_name"):
            if params.get("project_name") == "all":
                queryset = Q()
            else:
                queryset &= Q(project_name__icontains=params.get('project_name'))
        if params.get('report_type'):
            queryset &= Q(report_type=params.get('report_type'))
        project_list = TestReports.objects.values_list("project_name", flat=True).distinct()
        objs = TestReports.objects.filter(queryset).order_by('-create_time')
        paginator_objs = page_paginator(request, objs)
        serializer = TestReportsSerializer(paginator_objs, many=True)
        return Response({
            'data': serializer.data,
            'total': objs.count(),
            'status': status.HTTP_200_OK,
        }, status=status.HTTP_200_OK)
    """

    def create(self, request, *args, **kwargs):
        request_data = json.loads(request.body)
        serializer = TestReportsSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        obj = TestReports.objects.create(**request_data)
        return Response(status=status.HTTP_201_CREATED, data={"message": "create successfully", "data": TestReportsSerializer(obj).data, "status": status.HTTP_201_CREATED})

    def update(self, request, *args, **kwargs):
        request_data = json.loads(request.body)
        testreport_obj = self.get_object() # TestReports object (id)
        # recording Testing time
        previous_step = testreport_obj.run_step
        previous_test_end_time = testreport_obj.test_end_time
        # try to get run step and turn it to a int
        run_step = -1
        try:
            run_step = int(request_data.get("run_step", -1))
        except Exception as e:
            del request_data["run_step"]
            print("Run step should be int or strings format int.")
        if run_step in [4, 5, 6, 7]:
            if (previous_test_end_time == None):  # skip set end time when already have one
                request_data["test_end_time"] = datetime.datetime.now()
        # update components
        components = request_data.pop("components", {})
        try:
            for component in components.items():
                new_report_component.component_name = component[0]
                new_report_component.component_value = component[1]
                new_report_component = ReportComponent.objects.create(component_name=component[0], component_value=component[1], test_report_id=testreport_obj.id)
        except Exception:
            print('Error: failed to update components')
        TestReports.objects.filter(id=testreport_obj.id).update(**request_data)
        return Response({"message": "update successfully", "data": request_data}, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=True)
    def all_abort(self, request, *args, **kwargs):
        testreport_obj = self.get_object() # TestReports object (id)
        previous_test_end_time = testreport_obj.test_end_time
        test_case_run = TestCaseRun.objects.filter(test_report_id=testreport_obj.id)
        test_case_run.filter(status__in=[0, 1]).update(status=4)
        #must update the run step to 4
        testreport_obj.run_step = 4
        if (previous_test_end_time == None):  # skip set start time when already have one
            testreport_obj.test_end_time = datetime.datetime.now()
        testreport_obj.save()
        return Response({"message": "Abort all successfully", "data": ""}, status=status.HTTP_202_ACCEPTED)

class TestReportDetailView(viewsets.ModelViewSet):
    queryset = TestReports.objects.all()
    serializer_class = TestReportDetailSerializer
    pagination_class = MyPage # ??
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter] # ??
    filterset_fields = ('id', ) # django_filters
    search_fields = ('id', ) # ??
    ordering_fields = ('id', 'create_time') # ??
    ordering = ['-create_time'] # ??

    def update(self, request, *args, **kwargs):
        request_data = json.loads(request.body)
        testreport_obj = self.get_object() # TestReports object (id)
        request_comment = request_data.get('comment', '')
        run_status = request_data.get('status', -1)
        # search if any unfinished old test_case_run record
        old_test_case_run = testreport_obj.test_case_run.all().filter(testcase_name=request_data.get("testcase_name"), status__in=[0, 1])
        if run_status > 1 :
            if old_test_case_run:
                old_test_case_run.update(**request_data)
                return Response({"message": "Update old record Success", "data": old_test_case_run.data}, status=status.HTTP_201_CREATED)
        if not(TestServers.objects.filter(ip=request_data.get("serverip"))):
            testserver_obj = TestServers.objects.create(ip=request_data.get("serverip"))
        else:
            testserver_obj = TestServers.objects.get(ip=request_data.get("serverip"))
        new_test_case_run = TestCaseRun.objects.create(status=request_data['status'], test_server_id=testserver_obj.id,
                                                       comment=request_comment)
        testreport_obj.test_case_run.add(new_test_case_run)
        testreport_obj.save()
        new_testcase_data = TestCaseRunSerializer(new_test_case_run)
        return Response({"message": "Create Success", "data": new_testcase_data.data}, status=status.HTTP_201_CREATED)

    def patch(self, request, id):
        request_data = json.loads(request.body)
        testreport_obj = TestReports.objects.get(id=id)
        testreport_list = TestReports.objects.filter(project_name=testreport_obj.project_name,type=testreport_obj.type).order_by('-id')
        flag_previous_tesreport = False
        if len(testreport_list) > 1:
            previous_testreport_obj = testreport_list[1]
            flag_previous_tesreport = True
        if request_data.get("updateComment"):
            # did not wish update_time tobe changed by update comments, id becomes testcaserun id
            testcaserun_obj = TestCaseRun.objects.filter(id=request_data.get('id'))
            if len(testcaserun_obj) > 0 :
                testcaserun_obj.update(comment=request_data["comment"])
        else:
            # Because create TestCaseRun with None server in init, so if get test_server=None, need to update it first
            _none_server_testcaserun_obj = testreport_obj.test_case_run.all().filter(test_server=None, testcase__name=request_data.get("testcase"), asic=request_data.get("update_data").get("asic"), status=0)
            if len(_none_server_testcaserun_obj) != 0:
                test_case_run_obj = _none_server_testcaserun_obj[0]
                test_case_run_obj.test_server = TestServers.objects.get(ip=request_data.get("serverip"))
                test_case_run_obj.create_time = datetime.datetime.now()
                test_case_run_obj.save()
                testreport_obj.test_case_run.all().filter(id=test_case_run_obj.id).update(**request_data["update_data"])
            else:
                # filter server and case and asic, if exist, update it. if not, create
                _testcaserun_obj = testreport_obj.test_case_run.all().filter(test_server__ip=request_data.get("serverip"))
                if len(_testcaserun_obj) >= 1:
                    """
                    if request_data.get("update_data") and request_data.get("update_data").get("status") and int(request_data.get("update_data").get("status")) == 3:
                        # determine if this is regression
                        if flag_previous_tesreport:
                            previous_testcase_obj = previous_testreport_obj.test_case_run.all().filter(testcase_id=_testcaserun_obj[0].testcase_id, asic=_testcaserun_obj[0].asic)
                            if len(previous_testcase_obj) == 1 and previous_testcase_obj[0].status == 2:
                                request_data["update_data"]["status"] = 6
                    """
                    _testcaserun_obj.update(**request_data["update_data"])
                else:
                    _server_obj = TestServers.objects.get(ip=request_data.get("serverip"))
                    _new_testcaserun_obj = TestCaseRun.objects.create(test_server_id=_server_obj.id, **request_data["update_data"])
                    testreport_obj.test_case_run.add(_new_testcaserun_obj)
        return Response({"message": "Update Success", "data": request_data}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        print("this view does not support update function")
        return Response({})

class TestCaseRunView(viewsets.ModelViewSet):
    queryset = TestCaseRun.objects.all()
    serializer_class = TestCaseRunSerializer
    pagination_class = MyPage # ??
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter] # ??
    filterset_fields = ('id', 'testcase_name', 'test_report_id', 'status') # django_filters
    search_fields = ('id', 'testcase_name', 'test_report_id', 'status') # ??
    ordering_fields = ('id', 'create_time') # ??
    ordering = ['-create_time'] # ??

    def create(self, request, *args, **kwargs):
        request_data = json.loads(request.body)
        test_report = request_data.pop('test_report', 0)
        try:
            test_report_obj = TestReports.objects.get(id=test_report)
        except Exception as e:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={"message": f"Failed, testreport id: {test_report} not found.", "data": request_data, "status": status.HTTP_406_NOT_ACCEPTABLE})
        request_data["test_report_id"] = test_report
        # check if test_report finished
        test_report_run_status = test_report_obj.run_status
        test_report_run_step = test_report_obj.run_step
        if test_report_run_step > 3 or not test_report_run_status:
             return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={"message": f"Failed, testreport {test_report} is closed.", "data": request_data, "status": status.HTTP_406_NOT_ACCEPTABLE})
        serializer = TestCaseRunSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        obj = TestCaseRun.objects.create(**request_data)
        return Response(status=status.HTTP_201_CREATED, data={"message": "create successfully", "data": TestCaseRunSerializer(obj).data, "status": status.HTTP_201_CREATED})

    def update(self, request, *args, **kwargs):
        request_data = json.loads(request.body)
        print("this view does not support update function")
        return Response({})

    def delete(self, request, *args, **kwargs):
        print("this view does not support update function")
        return Response({})

class ReportComponentView(viewsets.ModelViewSet):
    queryset = ReportComponent.objects.all()
    serializer_class = ReportComponentSerializer
    pagination_class = MyPage # ??
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter] # ??
    filterset_fields = ('id', 'component_name', 'test_report_id') # django_filters
    search_fields = ('id', 'component_name', 'test_report_id') # ??
    ordering_fields = ('id', 'create_time') # ??
    ordering = ['-create_time'] # ??

    def create(self, request, *args, **kwargs):
        request_data = json.loads(request.body)
        test_report = request_data.pop('test_report', 0)
        try:
            test_report_obj = TestReports.objects.get(id=test_report)
        except Exception as e:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={"message": f"Failed, testreport id: {test_report} not found.", "data": request_data, "status": status.HTTP_406_NOT_ACCEPTABLE})
        request_data["test_report_id"] = test_report
        # check if test_report finished
        test_report_run_status = test_report_obj.run_status
        test_report_run_step = test_report_obj.run_step
        if test_report_run_step > 3 or not test_report_run_status:
             return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={"message": f"Failed, testreport {test_report} is closed.", "data": request_data, "status": status.HTTP_406_NOT_ACCEPTABLE})
        serializer = ReportComponentSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        obj = ReportComponent.objects.create(**request_data)
        return Response(status=status.HTTP_201_CREATED, data={"message": "create successfully", "data": TestCaseRunSerializer(obj).data, "status": status.HTTP_201_CREATED})

    def update(self, request, *args, **kwargs):
        request_data = json.loads(request.body)
        print("this view does not support update function")
        return Response({})

    def delete(self, request, *args, **kwargs):
        print("this view does not support update function")
        return Response({})
