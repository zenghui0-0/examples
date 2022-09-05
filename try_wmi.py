'''
pip install wmi
'''
import wmi
def sys_version(ip_address, username, password):
    conn = wmi.WMI(computer=ip_address, user=username, password=password)
    """
    for process in conn.Win32_Process ():
        print(process.ProcessId, process.Name)
    for sys in conn.Win32_OperatingSystem():
        print("Version:%s" % sys.Caption.encode("UTF8"),"Vernum:%s" % sys.BuildNumber)  #系统信息
        print(sys.OSArchitecture.encode("UTF8"))  # 系统的位数
        print(sys.NumberOfProcesses)  # 系统的进程数
    """
    id, value =conn.Win32_Process.Create(CommandLine="ipconfig")
    print(id,value)
 
if __name__ == '__main__':
    sys_version(ip_address="192.101.17.35", username="Administrator", password="password")
