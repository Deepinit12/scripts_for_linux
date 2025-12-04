import requests, time


last_ip = None
while True:
    ip = requests.get("https://api.ipify.org").text
    if ip != last_ip and last_ip is not None:
        print(f"[ALERT] IP changed: {last_ip} -> {ip}")
    last_ip = ip
    time.sleep(10)