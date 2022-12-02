# pip install pywinrm
#Port 5985 is opened and reachable

#Command Execution
import winrm

machine_ip = 'http://DESKTOP-KTD0A7A'
username = 'admin'
# username = r'DESKTOP-KTD0A7A\admin'
password = 'admin'


s = winrm.Session(
    machine_ip, auth=(username, password)
    )
r = s.run_cmd('ipconfig', ['/all'])
print (r.status_code)  #0
print (r.std_out)
'''
Windows IP Configuration

   Host Name . . . . . . . . . . . . : WINDOWS-HOST
   Primary Dns Suffix  . . . . . . . :
   Node Type . . . . . . . . . . . . : Hybrid
   IP Routing Enabled. . . . . . . . : No
   WINS Proxy Enabled. . . . . . . . : No

'''
print ( r.std_err)


#Run Powershell script on remote host
import winrm
ps_script = """$strComputer = $Host
Clear
$RAM = WmiObject Win32_ComputerSystem
$MB = 1048576

"Installed Memory: " + [int]($RAM.TotalPhysicalMemory /$MB) + " MB" """

s = winrm.Session('windows-host.example.com', auth=('john.smith', 'secret'))
r = s.run_ps(ps_script)
print (r.status_code)  #0
print (r.std_out)
'''
Installed Memory: 3840 MB
'''
print ( r.std_err)
