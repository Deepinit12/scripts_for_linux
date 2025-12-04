#!/usr/bin/env python3

import paramiko
import concurrent.futures
import sys

cmd = sys.argv[1]
hosts = sys.argv[2:]


def run(host):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username="root")
        stdin, stdout, stderr = ssh.exec_command(cmd)

        error = stderr.read().decode()
        if error:
            return host, f"Error: {error.strip()}"

        output = stdout.read().decode()
        return host, output.strip()

    except Exception as e:
        return host, f"[Exception] {str(e)}"    

with concurrent.futures.ThreadPoolExecutor() as ex:
    for host, out in ex.map(run, hosts):
        print(f"== {host} ==\n{out}")