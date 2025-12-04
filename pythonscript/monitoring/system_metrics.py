#!/usr/bin/env python3

import psutil
import time

try:
    while True:

        data = {
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
        }


        print(f" CPU:  {data['cpu']:5.1}%|"
              f" RAM: {data['ram']:5.1}% |"
              f" Disk: {data['disk']:5.1}%")

         time.sleep(5)

except KeyboardInterrupt:
    print("\nExiting...")