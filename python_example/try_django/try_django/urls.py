"""history_book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include, re_path
# ???view
from users.views import UsersView
from testreports.views import TestReportsView, TestReportDetailView, TestCaseRunView, ReportComponentView
from testservers.views import TestServerListView
# swagger????
from rest_framework import routers, permissions
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="try django Rest API",
        default_version="v1",
        description="????????",
        terms_of_service="#",
        contact=openapi.Contact(email="123456789@qq.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()  # ??????????
router.register(r'testreports', TestReportsView)
router.register(r'testreportDetail', TestReportDetailView)
router.register(r'testcaserun', TestCaseRunView)
router.register(r'reportcomponent', ReportComponentView)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'users/(.*)', UsersView.as_view()),
    url(r'testservers/(.*)', TestServerListView.as_view()),
    # url(r'testreports/(.*)', TestReportsView.as_view({'get': 'retrieve'})),
    # url(r'testreportDetail/(.*)', TestReportDetailView.as_view()),
    # ??drf-yasg??
    url(r"docs/", include_docs_urls(title="My API title")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api-auth/', include('rest_framework.urls'))，
]
urlpatterns += router.urls
