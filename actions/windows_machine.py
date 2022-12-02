import traceback
import sys
import winrm


read_timeout=120
write_timeout=60


machine_ip = '10.50.103.119'
username = r'admin'
password = 'admin'


"""
If you perform shutdwon on windows systems
    confirm this configuration on target machine

1 - windows winrm service should running
2 - cmd <run as administrator> winrm configSDDL default 
    - username should be added first
3 - cmd <run as administrator> winrm get winrm/config
    - port http (5985) listed
    - trustedhost should added
5 - add a user in the group to force shutdown
    type in: secpol.msc -> local policies -> User Rights Assignment -> force shutdown from a remote system
"""


def execute_shutdown():
    print(f"#"*50, "shuting down:", machine_ip)
    try:
        p = winrm.protocol.Protocol(
            endpoint='http://%s:5985/wsman' % machine_ip,
            transport='ntlm',
            username=username,
            password=password,
            server_cert_validation='ignore')
        shell_id = p.open_shell()
        # command_id = p.run_command(shell_id, 'ipconfig', ['/all'])
        # command_id = p.run_command(shell_id, 'shutdown', ['/l'])
        # command_id = p.run_command(shell_id, 'shutdown')
        command_id = p.run_command(shell_id, 'shutdown', ['/s', '/t 0'])
        # command_id = p.run_command(shell_id, 'shutdown', ['/s'])
        # command_id = p.run_command(shell_id, 'shutdown', ['/r'])
        std_out, std_err, status_code = p.get_command_output(shell_id, command_id)
        p.cleanup_command(shell_id, command_id)
        # print(std_out, status_code)
        print(f"status_code.... {status_code}")
        print(f"std_out.... {std_out.decode()}")
        print(f"std_err.... {std_err.decode()}\n\n")
        p.close_shell(shell_id)
    except Exception as exc:
        traceback.print_exc(file=sys.stdout)
        # traceback.print_exc(limit=1, file=sys.stdout)
        print(f"Error:{type(exc)} {exc}")



if __name__ == '__main__':
    execute_shutdown()