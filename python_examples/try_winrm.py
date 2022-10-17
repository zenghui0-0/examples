import winrm

s=winrm.Session('http://192.101.17.35:5985/wsman', auth=('Administrator','password'))

#r = s.run_cmd(b'C:\Users\Administrator\Desktop\conplyent_9922.bat')
r = s.run_cmd("dir")

print(r.std_out.decode())
print(r.std_err.decode())
print("end of connect")
