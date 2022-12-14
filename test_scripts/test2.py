import winrm
import traceback


read_timeout=120
write_timeout=60


machine_ip = '10.50.103.119'
username = r'admin'
password = 'admin'



def execute_action1():
    print(f"#"*50, "action_1")
    try:
        s = winrm.Session(
            machine_ip,
            auth=(username, password),
            read_timeout_sec=read_timeout,
            operation_timeout_sec=write_timeout,
        )
        r = s.run_cmd('ipconfig')
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
    except Exception as exc:
        traceback.print_exc(file=sys.stdout)
        # traceback.print_exc(limit=1, file=sys.stdout)
        print(f"Error action 1 {type(exc)} {exc}")
    print(f"#"*50)


def execute_action2():
    print(f"#"*50, "action_2")
    try:
        #Run Powershell script on remote host
        ps_script = """$strComputer = $Host
        Clear
        $RAM = WmiObject Win32_ComputerSystem
        $MB = 1048576

        "Installed Memory: " + [int]($RAM.TotalPhysicalMemory /$MB) + " MB" """

        s = winrm.Session(
            machine_ip,
            auth=(username, password),
            read_timeout_sec=read_timeout,
            operation_timeout_sec=write_timeout,
            # server_cert_validation='ignore',
            server_cert_validation='validate',
            credssp_disable_tlsv1_2=True,
        )
        r = s.run_ps(ps_script)
        print (r.status_code)  #0
        print (r.std_out)
        '''
        Installed Memory: 3840 MB
        '''
        print ( r.std_err)
    except Exception as exc:
        traceback.print_exc(file=sys.stdout)
        print(f"Error action 2: {exc}")
    print(f"#"*50)


def execute_action3():
    print(f"#"*50, "action_3")
    try:
        p = winrm.protocol.Protocol(
            # endpoint='http://10.50.103.119:3389/wsman',
            # endpoint='http://DESKTOP-KTD0A7A:3389/wsman',
            endpoint='%s/wsman' % machine_ip,
            transport='ntlm',
            username=username,
            password=password,
            server_cert_validation='validate',
            # server_cert_validation='ignore',
            read_timeout_sec=read_timeout,
            operation_timeout_sec=write_timeout,
        )
        
        shell_id = p.open_shell()
        command_id = p.run_command(shell_id, 'ipconfig', ['/all'])
        std_out, std_err, status_code = p.get_command_output(shell_id, command_id)
        print(f"status_code.... {status_code}")
        print(f"std_out.... {std_out}")
        print(f"std_err.... {std_err}")
        p.cleanup_command(shell_id, command_id)
        p.close_shell(shell_id)

    except Exception as exc:
        traceback.print_exc(file=sys.stdout)
        print(f"Error action 3: {exc}")
    print(f"#"*50)
