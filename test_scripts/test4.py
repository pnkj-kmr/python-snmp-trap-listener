from winrm.protocol import Protocol
import traceback
import sys
import json

"""
1 - windows winrm service started
2 - cmd <run as administrator> winrm configSDDL default
3 - added the user -- permission need to altered
4 - http port(5985) allowed
5 - added user in the group
    type in: secpol.msc -> local policies -> User Rights Assignment -> force shutdown from a remote system
"""

try:
    p = Protocol(
        endpoint='http://10.50.103.119:5985/wsman',
        transport='ntlm',
        username=r'admin',
        password='admin',
        server_cert_validation='ignore')
    shell_id = p.open_shell()
    # command_id = p.run_command(shell_id, 'ipconfig', ['/all'])
    # command_id = p.run_command(shell_id, 'shutdown', ['/l'])
    # command_id = p.run_command(shell_id, 'shutdown')
    # command_id = p.run_command(shell_id, 'shutdown', ['/s'])
    command_id = p.run_command(shell_id, 'shutdown', ['/r'])
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

