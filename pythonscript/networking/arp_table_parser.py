import subprocess
import re


arp = subprocess.check_output(["arp", "-a"]).decode()
for line in arp.splitlines():
match = re.findall(r"(\S+) \((.*?)\) at (.*?) ", line)
if match:
print(match[0])