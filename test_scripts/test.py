import traceback
import sys
import winrm

# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     # Legacy Python that doesn't verify HTTPS certificates by default
#     pass
# else:
#     # Handle target environment that doesn't support HTTPS verification
#     ssl._create_default_https_context = _create_unverified_https_context


read_timeout=120
write_timeout=60


# machine_ip = 'https://10.50.103.119:3389'
# machine_ip = 'http://DESKTOP-KTD0A7A:3389'
machine_ip = '10.50.103.119'
# username = 'admin'
# username = "DESKTOP-KTD0A7A\\Admin"
username = r'DESKTOP-KTD0A7A\admin'
# username = 'admin'
password = 'admin'

print(f"#"*50, "test")
try:
    s = winrm.Session(
        machine_ip,
        auth=(username, password),
        read_timeout_sec=read_timeout,
        operation_timeout_sec=write_timeout,
        server_cert_validation='ignore',
        # server_cert_validation='validate',
        # credssp_disable_tlsv1_2=True,
    )
    print("......session", s)
    r = s.run_cmd('ipconfig')
    print("......cmd", r)
    print ('....status', r.status_code)  #0
    print ('....std_out', r.std_out)
    '''
    Windows IP Configuration

    Host Name . . . . . . . . . . . . : WINDOWS-HOST
    Primary Dns Suffix  . . . . . . . :
    Node Type . . . . . . . . . . . . : Hybrid
    IP Routing Enabled. . . . . . . . : No
    WINS Proxy Enabled. . . . . . . . : No

    '''
    print ('....std_err', r.std_err)
except Exception as exc:
    traceback.print_exc(file=sys.stdout)
    # traceback.print_exc(limit=1, file=sys.stdout)
    print(f"Error action 1 {type(exc)} {exc}")
print(f"#"*50)


