from django.shortcuts import render
from rest_framework import viewsets
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializer import TestReportSimpleSerializer
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt
from utils.tools import page_paginator
from .models import TestReports
import datetime
import json


# Create your views here.
class TestReportsView(GenericAPIView):
    serializer_class = TestReportSimpleSerializer

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
        serializer = TestReportSimpleSerializer(paginator_objs, many=True)
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
        serializer = TestReportSimpleSerializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        obj = TestReports.objects.create(**post_data)
        return Response(status=status.HTTP_201_CREATED, data={"message": "create successfully", "data": TestReportSimpleSerializer(obj).data, "status": status.HTTP_201_CREATED})

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
        # the method that save benchmark score, follow rule that first come first save
        # performance data structure:
        # {
        #  "windows": [{"name":"benchmark 1", "score":100}, {"name":"benchmark 2", "score":200}],
        #  "ubuntu": [{"name":"benchmark 3", "score":300}, {"name":"benchmark 4", "score":400}]
        # }
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
