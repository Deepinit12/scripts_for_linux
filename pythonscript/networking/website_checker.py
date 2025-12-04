#!/usr/bin/env python3
import requests
import time
import sys

if len(sys.argv) < 2:
    print("Использование: python3 check_site.py <URL>")
    print("Пример: python3 check_site.py https://google.com")
    sys.exit(1)

url = sys.argv[1]
print(f"Проверяем доступность: {url}")

for attempt in range(5):
    try:
        r = requests.get(url, timeout=2)
        print(f"Попытка {attempt + 1}: Статус {r.status_code}")
        if r.status_code == 200:
            print(f"✅ Сайт доступен! Ответ за {r.elapsed.total_seconds():.2f} сек")
            break
    except requests.exceptions.Timeout:
        print(f"Попытка {attempt + 1}: ⏰ Таймаут")
    except requests.exceptions.ConnectionError:
        print(f"Попытка {attempt + 1}: 🔌 Ошибка подключения")
    except Exception as e:
        print(f"Попытка {attempt + 1}: ❌ Ошибка: {e}")
    
    if attempt < 4:  # Не ждать после последней попытки
        time.sleep(1)
else:
    print(f"❌ Не удалось подключиться к {url} после 5 попыток")