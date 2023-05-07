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
from .models import TestReports, TestCaseRun
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
            elif request.GET.get("project_name") == "presubmission":
                queryset &= Q(type=1)
            else:
                queryset &= Q(project_name__icontains=request.GET.get('project_name')) & ~Q(type=1)
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
        report_obj = TestReports.objects.get(id=id)
        # recording Testing time
        previous_step = report_obj.run_step
        previous_test_end_time = report_obj.test_end_time
        # try to get run step and turn it to a int
        run_step = -1
        try:
            run_step = int(request_data.get("run_step"))
        except Exception as e:
            print("Run step should be int or strings format int.")
        if run_step in [4, 5, 6, 7]:
            if (previous_test_end_time == None):  # skip set end time when already have one
                request_data["test_end_time"] = datetime.datetime.now()
        if request_data.get("all_abort"):
            report_obj.test_case_run.all().filter(status__in=[0, 1]).update(status=4)
            #must update the run step to 4
            report_obj.run_step = 4
            report_obj.save()
            if (previous_test_end_time == None):  # skip set start time when already have one
                TestReports.objects.filter(id=id).update(test_end_time=datetime.datetime.now())
            return Response({"message": "Abort all successfully", "data": request_data}, status=status.HTTP_202_ACCEPTED)
        if request_data.get("components"):
            if report_obj.components:
                existed_components = json.loads(report_obj.components.replace("'", "\""))
                for _k in request_data.get("components").keys():
                    if _k in existed_components:
                        existed_components[_k] = existed_components[_k] + ";"+request_data.get("components").get(_k)
                    else:
                        existed_components[_k] = request_data.get("components").get(_k)
                request_data["components"] = json.dumps(existed_components)
        if request_data.get("benchmark_score"):
            if not report_obj.comment:
                report_obj.comment = '{"performance":{}}'
            origin_data = json.loads(report_obj.comment)
            if not origin_data.get("performance"):
                origin_data["performance"] = {}
            performance_data = origin_data.get("performance")
            for _item in request_data.get("benchmark_score"):
                if _item["guest_os"] not in performance_data.keys():
                    performance_data[_item["guest_os"]] = []
                benchmark_list = [item["name"] for item in performance_data[_item["guest_os"]]]
                if _item["name"] not in benchmark_list:
                    performance_data[_item["guest_os"]].append({"name": _item["name"], "score": int(_item["avg_score"])})
            origin_data["performance"] = performance_data
            report_obj.comment = json.dumps(origin_data)
            report_obj.save()
            return Response({"message": "update successfully", "data": request_data}, status=status.HTTP_201_CREATED)
        TestReports.objects.filter(id=id).update(**request_data)
        return Response({"message": "update successfully", "data": request_data}, status=status.HTTP_201_CREATED)

    @method_decorator(permission_required('testreport.delete_testreport', raise_exception=True))
    def delete(self, request, id):
        post_data = json.loads(request.body)
        obj = TestReports.objects.get(id=post_data['id'])
        obj.delete()
        return Response(post_data, status=status.HTTP_200_OK)


class TestReportDetailView(GenericAPIView):
    serializer_class = TestReportDetailSerializer

    def get(self, request, id):
        queryset = Q(id=id)
        obj_report = TestReports.objects.get(queryset)
        objs_case = obj_report.test_case_run.all()
        # num_objs_case = objs_case.values_list("testcase__name", flat=True).distinct()
        report_data = TestReportDetailSerializer(obj_report)
        return Response({
            'data': report_data.data,
            'total': len(objs_case),
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
        if not(TestServers.objects.filter(hostname=request_data.get("test_server"))):
            testserver_obj = TestServers.objects.create(hostname=request_data.get("test_server"))
        else:
            testserver_obj = TestServers.objects.get(hostname=request_data.get("test_server"))
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
            #did not wish update_time tobe changed by update comments
            testcaserun_obj = TestCaseRun.objects.filter(id=request_data.get('id'))
            if len(testcaserun_obj) >0 :
                testcaserun_obj.update(comment=request_data["comment"])
        else:
            # Because create TestCaseRun with None server in init, so if get test_server=None, need to update it first
            _none_server_testcaserun_obj = testreport_obj.test_case_run.all().filter(test_server=None, testcase__name=request_data.get("testcase"), asic=request_data.get("update_data").get("asic"), status=0)
            if len(_none_server_testcaserun_obj) != 0:
                test_case_run_obj = _none_server_testcaserun_obj[0]
                test_case_run_obj.test_server = TestServer.objects.get(hostname=request_data.get("testserver"))
                test_case_run_obj.create_time = datetime.datetime.now()
                test_case_run_obj.save()
                testreport_obj.test_case_run.all().filter(id=test_case_run_obj.id).update(**request_data["update_data"])
            else:
                # filter server and case and asic, if exist, update it. if not, create
                _testcaserun_obj = testreport_obj.test_case_run.all().filter(test_server__hostname=request_data.get("testserver"))
                if len(_testcaserun_obj) >= 1:
                    if request_data.get("update_data") and request_data.get("update_data").get("status") and int(request_data.get("update_data").get("status")) == 3:
                        # determine if this is regression
                        if flag_previous_tesreport:
                            previous_testcase_obj = previous_testreport_obj.test_case_run.all().filter(testcase_id=_testcaserun_obj[0].testcase_id, asic=_testcaserun_obj[0].asic)
                            if len(previous_testcase_obj) == 1 and previous_testcase_obj[0].status == 2:
                                request_data["update_data"]["status"] = 6
                    _testcaserun_obj.update(**request_data["update_data"])
                else:
                    _server_obj = TestServers.objects.get(hostname=request_data.get("testserver"))
                    _new_testcaserun_obj = TestCaseRun.objects.create(test_server_id=_server_obj.id, **request_data["update_data"])
                    testreport_obj.test_case_run.add(_new_testcaserun_obj)
        return Response({"message": "Update Success", "data": request_data}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        return Response({"message": "Delete Successfully"}, status=status.HTTP_200_OK)

