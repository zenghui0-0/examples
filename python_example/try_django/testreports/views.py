from django.shortcuts import render
from rest_framework import viewsets
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializer import TestReportsSerializer, TestReportDetailSerializer, TestCaseRunSerializer
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt
from utils.tools import page_paginator
from .models import TestReports, TestCaseRun, ReportComponent
from testservers.models import TestServers
from users.models import Users
import datetime
import json


# Create your views here.
class TestReportsView(GenericAPIView):
    serializer_class = TestReportsSerializer

    def get(self, request, id):
        queryset = Q()
        if request.GET.get("id"):
            queryset &= Q(id=request.GET.get("id"))
        if request.GET.get("project_name"):
            if request.GET.get("project_name") == "all":
                queryset = Q()
            else:
                queryset &= Q(project_name__icontains=request.GET.get('project_name'))
        if request.GET.get('report_type'):
            queryset &= Q(report_type=request.GET.get('report_type'))

        if request.GET.get('type'):
            queryset &= Q(report_type=request.GET.get('type'))
        project_list = TestReports.objects.values_list("project_name", flat=True).distinct()
        objs = TestReports.objects.filter(queryset).order_by('-create_time')
        paginator_objs = page_paginator(request, objs)
        serializer = TestReportsSerializer(paginator_objs, many=True)
        return Response({
            'data': serializer.data,
            'total': objs.count(),
            'status': status.HTTP_200_OK,
        }, status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request, id):
        post_data = request.POST.dict()
        print(post_data)
        # del post_data['csrfmiddlewaretoken']
        serializer = TestReportsSerializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        obj = TestReports.objects.create(**post_data)
        return Response(status=status.HTTP_201_CREATED, data={"message": "create successfully", "data": TestReportsSerializer(obj).data, "status": status.HTTP_201_CREATED})

    def patch(self, request, id):
        request_data = json.loads(request.body)
        testreport_obj = TestReports.objects.get(id=id)
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
        if request_data.get("all_abort"):
            testreport_obj.test_case_run.all().filter(status__in=[0, 1]).update(status=4)
            #must update the run step to 4
            testreport_obj.run_step = 4
            testreport_obj.save()
            if (previous_test_end_time == None):  # skip set start time when already have one
                TestReports.objects.filter(id=id).update(test_end_time=datetime.datetime.now())
            return Response({"message": "Abort all successfully", "data": request_data}, status=status.HTTP_202_ACCEPTED)
        # update components
        components = request_data.get("components", {})
        try:
            for component in components.items():
                new_report_component.component_name = component[0]
                new_report_component.component_value = component[1]
                new_report_component = ReportComponent.objects.create(component_name=component[0], component_value=component[1], test_report_id=id)
        except Exception:
            print('Error: failed to update components')
        TestReports.objects.filter(id=id).update(**request_data)
        return Response({"message": "update successfully", "data": request_data}, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        post_data = json.loads(request.body)
        obj = TestReports.objects.get(id=post_data['id'])
        obj.delete()
        return Response(post_data, status=status.HTTP_200_OK)


class TestReportDetailView(GenericAPIView):
    serializer_class = TestReportDetailSerializer

    def get(self, request, id):
        queryset = Q()
        report_id = try_get_id(request, id)
        if report_id is None:
            return Response({"message": "Failed: No report id.", "data": {},
                             'status': status.HTTP_404_NOT_FOUND})
        queryset &= Q(id=report_id)
        obj_report = TestReports.objects.get(queryset)
        report_data = TestReportDetailSerializer(obj_report)
        return Response({
            'data': report_data.data,
            'status': status.HTTP_200_OK,
        }, status=status.HTTP_200_OK)


    def post(self, request, id):
        request_data = json.loads(request.body)
        testreport_obj = TestReports.objects.get(id=id)
        request_comment = request_data.get('comment', '')
        run_status = request_data.get('status', -1)
        # search if any unfinished old test_case_run record
        old_test_case_run = testreport_obj.test_case_run.all().filter(name=request_data.get("Name"), status__in=[0, 1])
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

    def delete(self, request, id):
        return Response({"message": "Delete Successfully"}, status=status.HTTP_200_OK)


def try_get_id(request, id):
    # first we try to get id from request, when failed, try to turn id to int
    new_id = request.GET.get("id", None)
    try:
        new_id = int(new_id)
    except Exception as request_id_err:
        print(f"failed to get an int id from request, error: {request_id_err}.")
        try:
            new_id = int(id)
        except Exception as id_err:
            new_id = None
            print(f"failed to turn id to int, error: {id_err}.")
    return new_id
