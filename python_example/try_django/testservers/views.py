from django.shortcuts import render, get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from utils.tools import page_paginator
from .models import TestServers
from testreports.models import TestReports
from .serializer import TestServerSerializer
import datetime
import json

# Create your views here.
class TestServerListView(GenericAPIView):
    serializer_class = TestServerSerializer

    def get(self, request, id):
        #try to get id
        try:
            server_id = int(id)
            queryset = Q(id=server_id)
        except Exception as e:
            queryset = Q()
        if request.GET.get('name'):
            queryset &= Q(hostname__icontains=request.GET.get('name'))
        if request.GET.get("hostname"):
            queryset &= Q(hostname__icontains=request.GET.get('hostname'))
        if request.GET.get('server_type'):
            queryset &= Q(server_type=request.GET.get('server_type'))
        if request.GET.get("server_ip"):
            queryset &= Q(ip=request.GET.get('server_ip'))
        if request.GET.get('jenkins_node'):
            queryset &= Q(jenkins_node=request.GET.get('jenkins_node'))
        objs = TestServers.objects.filter(queryset).order_by('-update_time')
        paginator_objs = page_paginator(request, objs)
        serializer = TestServerSerializer(paginator_objs, many=True)
        return Response({
            'data': serializer.data,
            'total': objs.count(),
            'status': status.HTTP_200_OK,
        }, status=status.HTTP_200_OK)

    def post(self, request, id):
        post_data = json.loads(request.body)
        jenkins_node = post_data.get('jenkins_node')
        hostname = post_data.get('hostname')
        report_id =post_data.pop("report_id", 0)
        serializer = TestServerSerializer(data=post_data)
        if hostname:
            ServerList = TestServers.objects.filter(hostname=hostname)
            if (len(ServerList) > 0):
                ServerList.update(**post_data)
            else:
                TestServers.objects.create(**post_data)
        if report_id and hostname:
            testserver_id = TestServers.objects.get(hostname=hostname).id
            report_obj = TestReports.objects.get(id=report_id)
            previous_test_start_time = report_obj.test_start_time
            if (previous_test_start_time == None):  # skip set start time when already have one
                report_obj.test_start_time = datetime.datetime.now()
                report_obj.save()
        if serializer.is_valid():
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'data': serializer.errors}, status=status.HTTP_417_EXPECTATION_FAILED)
            data = serializer.errors


    def patch(self, request, id):
        request_data = json.loads(request.body)
        report_id = request_data.pop("report_id", 0)
        TestServers.objects.filter(hostname=request_data["hostname"]).update(**request_data)
        return Response(request_data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        request_data = json.loads(request.body)
        testserver_obj = get_object_or_404(TestServers, id=request_data.get('id'))
        testserver_obj.delete()
        return Response({"message": "Delete Success", "data":TestServerSerializer(testserver_obj).data}, status=status.HTTP_204_NO_CONTENT)
