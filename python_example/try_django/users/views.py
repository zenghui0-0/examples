from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from utils.tools import page_paginator
from .serializer import UserSerializer
from .models import Users


# Create your views here.
class UsersView(GenericAPIView):

    def get(self, request):
        queryset = Q()
        if request.GET.get("username"):
            queryset &= Q(username=request.GET.get("username"))
        if request.GET.get('email'):
            queryset &= Q(email=request.GET.get("email"))
        if request.GET.get('id'):
            queryset &= Q(id=request.GET.get("id"))
        objs = Users.objects.filter(queryset)
        paginator_objs = page_paginator(request, objs)
        serializer = UserSerializer(paginator_objs, many=True)
        return Response({
            'data': serializer.data,
            'total': objs.count(),
            'status': status.HTTP_200_OK,
        }, status=status.HTTP_200_OK)
