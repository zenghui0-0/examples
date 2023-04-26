from django.shortcuts import render
from rest_framework import viewsets
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializer import TestReportSimpleSerializer
from django.views.decorators.csrf import csrf_exempt
from utils.tools import page_paginator
from .models import TestReports
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
        request_data = json.loads(request.data)
        report_obj = TestReport.objects.get(id=id)
        return Response({"message": "update successfully", "data": request_data}, status=status.HTTP_201_CREATED)