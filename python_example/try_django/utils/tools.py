from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import requests

def page_paginator(request, objs):
    page_size = request.GET.get('pageSize', 20)
    page = request.GET.get('page', 1)
    if page_size == '0' and page == '0':
        return objs
    paginator = Paginator(objs, page_size)
    try:
        contexts = paginator.page(page)
    except PageNotAnInteger:
        contexts = paginator.page(1)
        return contexts.object_list
    except EmptyPage:
        contexts = paginator.page(paginator.num_pages)
        return contexts.object_list
    return contexts.object_list
