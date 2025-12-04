import re
from collections import Counter

errors = []
with open("/var/log/syslog") as f:
    lines = f.readlines()
    for line in reversed(lines):
        if "error" in line.lower():
            match = re.search(r"\[(.*?)\]", line)
            errors.append(match.group(1) if match else "Unknown")

for err, cnt in Counter(errors).most_common(10):
    print(err, cnt)         
            