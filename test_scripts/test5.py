import winrm
import traceback
import sys


TARGET_SYSTEMS = [
    {
        'machine_ip': '192.168.0.145',
        'username': r'bpets',
        'password': '2022',
    }
]


def calling_action(targets):
    for s in targets:
        execute_shutdown(s['machine_ip'], s['username'], s['password'])


def execute_shutdown(machine_ip, username, password):
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
    calling_action(TARGET_SYSTEMS)