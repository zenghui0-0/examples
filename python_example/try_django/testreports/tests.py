from django.test import TestCase
import requests
import socket
import json
import sys

# Create your tests here.
TEST_REPORT_TYPE = (
    (0, 'others'),
    (1, 'pre-submission'),
    (2, 'daily'),
    (3, 'weekly'),
    (4, 'release'),
)

def catch_exception(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print("Exception in test.py: {}".format(e))
    return wrapper

@catch_exception
def get_testreport(*args):
    report_id = int(args[0])
    apis = "{0}/testreport/?id={1}".format(host_name, report_id)
    res_get = requests.get(url=apis, headers=head, timeout=5)
    if res_get.status_code == 200:
        print(res_get.text)
    else:
        print("")


@catch_exception
def create_testreport(*args):
    apis = "{0}/testreport/".format(host_name)
    project_name, project_type, jenkins_url, artifactory_url, requester = \
        args[0], args[1], args[2], args[3], args[4]
    post_data = {"project_name": project_name, "jenkins_url": jenkins_url, "requester_ip": requester_ip,
                 "artifactory_url": artifactory_url, "type": TEST_REPORT_TYPE[project_type], "requester": requester}
    res_post = requests.post(url=apis, headers=head,
                        data=json.dumps(post_data), timeout=10)
    if res_post.status_code == 201:
        print("report_id={0}".format(json.loads(res_post.text)["data"]["id"]))
    # create one new report and save report id
    # parse all test case into report
    # Update report status
    # update testcase status


@catch_exception
def update_testreport_step(*args):
    report_id, run_status, run_step = args[0], args[1], args[2]
    apis = "{0}/testreport/{1}".format(host_name, report_id)
    post_data = {"run_step": run_step, "run_status": run_status}
    print("post_data in update_testreport_step:{0}".format(post_data))
    res = requests.patch(url=apis, headers=head,
                         data=json.dumps(post_data), timeout=5)
    print(res.status_code)


@catch_exception
def init_testcaselist(*args):
    report_id, test_case_list, asic, os_, hypervisor, guest_type = \
        args[0], args[1], args[2], args[3], args[4], args[5]
    apis = "{0}/testreportDetail/{1}".format(host_name, report_id)
    test_case_list = json.loads(test_case_list)
    post_data = {"test_case_list": test_case_list, "status": 0, "init": True,
                 "asic": asic, "os": os_, "guest_type": guest_type, "hypervisor": hypervisor}
    print("post_data in init_testcaselist:{0}".format(post_data))
    res = requests.post(url=apis, headers=head,
                        data=json.dumps(post_data), timeout=5)
    print(res.status_code)


@catch_exception
def update_testcase_run_status(*args):
    report_id, testcasename, status, node_name, servername, asic, os_, hypervisor, guest_type = \
        args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8]
    apis = "{0}/testreportDetail/{1}".format(host_name, report_id)
    update_data = {"status": status, "asic": asic, "os": os_,
                   "guest_type": guest_type, "hypervisor": hypervisor}
    post_data = {"node_name": node_name, "testserver": servername,
                 "testcase": testcasename, "update_data": update_data}
    print("post_data in update_testcase_run_status:{0}".format(post_data))
    res = requests.patch(url=apis, headers=head,
                         data=json.dumps(post_data), timeout=5)
    print("status_code:{0}".format(res.status_code))


@catch_exception
def update_testcase_report(*args):
    report_id, testcase_name, node_name, servername, report_url, detail_url, asic, os_, hypervisor, guest_type = \
        args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9]
    if detail_url == '""':
        detail_url = None
    apis = "{0}/testreportDetail/{1}".format(host_name, report_id)
    update_data = {"test_report_url": report_url, "detail_url": detail_url,
                   "asic": asic, "os": os_, "guest_type": guest_type}
    post_data = {"node_name": node_name, "testserver": servername,
                 "testcase": testcase_name, "update_data": update_data}
    print("post_data in update_testcase_report:{0}".format(post_data))
    res = requests.patch(url=apis, headers=head,
                         data=json.dumps(post_data), timeout=5)
    print("status_code:{0}".format(res.status_code))


@catch_exception
def update_all_case_abort(*args):
    report_id = args[0]
    apis = "{0}/testreport/{1}".format(host_name, report_id)
    post_data = {"all_abort": True}
    res = requests.patch(url=apis, headers=head,
                         data=json.dumps(post_data), timeout=5)
    print(res.status_code)


@catch_exception
def update_component(*args):
    report_id, servername, component = args[0], args[1], args[2]
    apis = "{0}/testreport/{1}".format(host_name, report_id)
    post_data = {"components": {servername: component}}
    print("post_data in update_component:{0}".format(post_data))
    res = requests.patch(url=apis, headers=head,
                         data=json.dumps(post_data), timeout=5)
    print("status_code:{0}".format(res.status_code))



if __name__ == "__main__":
    fun_name = sys.argv[1]
    args = tuple(sys.argv[2:])
    requester_ip = socket.gethostbyname(socket.gethostname())
    token = "Token 123412354wsdrfqawerqasdtr123235412341234"
    host_name = "http://10.21.16.245:8000/api/v1"
    head = {"Content-Type": "application/json; charset=UTF-8",
            "Authorization": token}
    globals().get(fun_name)(*args)
