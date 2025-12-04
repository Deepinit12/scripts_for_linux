#!/usr/bin/env python3
"""
Redis Queue Monitor - мониторинг очередей Redis в реальном времени
"""

import redis
import time
import argparse
import sys
from datetime import datetime
from typing import Dict, List, Optional
import json

class RedisQueueMonitor:
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        """Инициализация подключения к Redis"""
        try:
            self.client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True,  # Автоматически декодируем строки
                socket_timeout=5,
                socket_connect_timeout=5
            )
            # Проверяем подключение
            self.client.ping()
            print(f"✅ Подключено к Redis {host}:{port} (DB:{db})")
        except redis.ConnectionError:
            print(f"❌ Не удалось подключиться к Redis {host}:{port}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            sys.exit(1)
    
    def get_queue_info(self, queue_name: str) -> Dict:
        """Получает информацию об очереди"""
        try:
            queue_type = self.client.type(queue_name)
            
            if queue_type == 'list':
                size = self.client.llen(queue_name)
                # Получаем несколько элементов для анализа
                first_elem = self.client.lrange(queue_name, 0, 0)
                last_elem = self.client.lrange(queue_name, -1, -1)
                
                return {
                    'type': 'list',
                    'size': size,
                    'first_element': first_elem[0] if first_elem else None,
                    'last_element': last_elem[0] if last_elem else None
                }
            
            elif queue_type == 'stream':
                # Для Redis Streams
                size = self.client.xlen(queue_name)
                return {
                    'type': 'stream',
                    'size': size
                }
            
            elif queue_type == 'set':
                # Для Set (неупорядоченная очередь)
                size = self.client.scard(queue_name)
                return {
                    'type': 'set',
                    'size': size
                }
            
            else:
                return {
                    'type': queue_type or 'empty',
                    'size': 0
                }
                
        except Exception as e:
            return {'error': str(e)}
    
    def get_all_queues(self, pattern: str = "*") -> List[str]:
        """Получает все ключи, похожие на очереди"""
        try:
            all_keys = self.client.keys(pattern)
            queues = []
            
            for key in all_keys:
                key_type = self.client.type(key)
                if key_type in ['list', 'stream', 'set']:
                    queues.append(key)
            
            return sorted(queues)
        except:
            return []
    
    def get_redis_info(self) -> Dict:
        """Получает общую информацию о Redis"""
        try:
            info = self.client.info()
            return {
                'used_memory': info.get('used_memory_human', 'N/A'),
                'connected_clients': info.get('connected_clients', 0),
                'total_commands_processed': info.get('total_commands_processed', 0),
                'uptime': info.get('uptime_in_seconds', 0),
                'keyspace': info.get('db0', {})
            }
        except:
            return {}
    
    def monitor_queue(self, queue_name: str, interval: float = 1.0, 
                     history_size: int = 60, show_elements: bool = False):
        """Мониторинг очереди в реальном времени"""
        print(f"🔍 Мониторинг очереди: {queue_name}")
        print(f"📊 Интервал обновления: {interval} сек")
        print("-" * 50)
        
        history = []  # История размеров для графика
        
        try:
            while True:
                # Получаем информацию об очереди
                queue_info = self.get_queue_info(queue_name)
                
                if 'error' in queue_info:
                    print(f"❌ Ошибка: {queue_info['error']}")
                    time.sleep(interval)
                    continue
                
                current_size = queue_info['size']
                history.append(current_size)
                
                # Ограничиваем историю
                if len(history) > history_size:
                    history.pop(0)
                
                # Очищаем экран и выводим информацию
                print("\033[2J\033[H", end="")  # Очистка экрана
                
                # Общая информация
                redis_info = self.get_redis_info()
                print(f"🕒 {datetime.now().strftime('%H:%M:%S')}")
                print(f"📊 Размер очереди: {current_size}")
                print(f"📈 История (последние {len(history)}): {history}")
                
                # Простой график ASCII
                if history:
                    max_val = max(history) if max(history) > 0 else 1
                    scale = 20 / max_val
                    
                    print("\n📈 График размера очереди:")
                    for val in history[-20:]:  # Последние 20 значений
                        bar_length = int(val * scale)
                        bar = "█" * bar_length + " " * (20 - bar_length)
                        print(f"  [{bar}] {val}")
                
                # Показываем элементы если нужно
                if show_elements and queue_info.get('first_element'):
                    print(f"\n📝 Первый элемент: {queue_info['first_element'][:100]}...")
                    print(f"📝 Последний элемент: {queue_info['last_element'][:100]}...")
                
                # Информация о Redis
                print(f"\n⚡ Redis:")
                print(f"  Подключения: {redis_info.get('connected_clients', 'N/A')}")
                print(f"  Память: {redis_info.get('used_memory', 'N/A')}")
                print(f"  Аптайм: {redis_info.get('uptime', 0)} сек")
                
                print("\n" + "=" * 50)
                print("Нажмите Ctrl+C для выхода")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n\n📊 Статистика за сеанс:")
            if history:
                print(f"  Минимальный размер: {min(history)}")
                print(f"  Максимальный размер: {max(history)}")
                print(f"  Средний размер: {sum(history)/len(history):.1f}")
            print("Мониторинг остановлен")
    
    def analyze_queue(self, queue_name: str):
        """Анализирует содержимое очереди"""
        print(f"🔍 Анализ очереди: {queue_name}")
        
        queue_info = self.get_queue_info(queue_name)
        
        if 'error' in queue_info:
            print(f"❌ Ошибка: {queue_info['error']}")
            return
        
        print(f"Тип: {queue_info['type']}")
        print(f"Размер: {queue_info['size']}")
        
        if queue_info['type'] == 'list' and queue_info['size'] > 0:
            # Анализируем несколько элементов
            print("\n📊 Анализ элементов:")
            
            # Берем первые 10 элементов
            elements = self.client.lrange(queue_name, 0, 9)
            
            for i, elem in enumerate(elements):
                print(f"{i+1:3}. ", end="")
                
                try:
                    # Пытаемся распарсить JSON
                    data = json.loads(elem)
                    if isinstance(data, dict):
                        print(f"JSON: {json.dumps(data, ensure_ascii=False)[:80]}...")
                    else:
                        print(f"Value: {str(data)[:80]}...")
                except:
                    print(f"Text: {elem[:80]}...")
        
        print(f"\n⏱️  Время обработки (оценка):")
        if queue_info['size'] > 100:
            print(f"  При скорости 10 эл/сек: {queue_info['size']/10:.1f} сек")
            print(f"  При скорости 100 эл/сек: {queue_info['size']/100:.1f} сек")
    
    def clear_queue(self, queue_name: str, confirm: bool = True):
        """Очищает очередь"""
        if confirm:
            response = input(f"⚠️  Очистить очередь '{queue_name}'? [y/N]: ")
            if response.lower() != 'y':
                print("Отменено")
                return
        
        size = self.client.delete(queue_name)
        print(f"✅ Очередь '{queue_name}' очищена")

def main():
    parser = argparse.ArgumentParser(
        description="Redis Queue Monitor - мониторинг и анализ очередей Redis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s queue_name                # Мониторинг одной очереди
  %(prog)s -l                        # Список всех очередей
  %(prog)s queue_name -a            # Анализ очереди
  %(prog)s queue_name -i 0.5       # Мониторинг с интервалом 0.5 сек
  %(prog)s queue_name -e            # Показывать элементы
  %(prog)s queue_name --clear       # Очистить очередь
  %(prog)s -H 192.168.1.100 -p 6380 # Подключение к удаленному Redis
        """
    )
    
    parser.add_argument("queue", nargs="?", help="Имя очереди для мониторинга")
    parser.add_argument("-l", "--list", action="store_true", help="Показать все очереди")
    parser.add_argument("-a", "--analyze", action="store_true", help="Анализировать очередь")
    parser.add_argument("-i", "--interval", type=float, default=1.0, help="Интервал обновления (сек)")
    parser.add_argument("-e", "--elements", action="store_true", help="Показывать элементы очереди")
    parser.add_argument("--clear", action="store_true", help="Очистить очередь")
    
    # Параметры подключения
    parser.add_argument("-H", "--host", default="localhost", help="Хост Redis")
    parser.add_argument("-p", "--port", type=int, default=6379, help="Порт Redis")
    parser.add_argument("-d", "--db", type=int, default=0, help="Номер базы данных")
    parser.add_argument("-P", "--password", help="Пароль Redis")
    
    args = parser.parse_args()
    
    # Создаем монитор
    monitor = RedisQueueMonitor(
        host=args.host,
        port=args.port,
        db=args.db,
        password=args.password
    )
    
    if args.list:
        # Показываем все очереди
        queues = monitor.get_all_queues()
        if queues:
            print(f"📋 Найдено {len(queues)} очередей:")
            for queue in queues:
                info = monitor.get_queue_info(queue)
                print(f"  • {queue} ({info['type']}): {info['size']} элементов")
        else:
            print("📭 Очереди не найдены")
    
    elif args.queue:
        if args.analyze:
            monitor.analyze_queue(args.queue)
        elif args.clear:
            monitor.clear_queue(args.queue)
        else:
            monitor.monitor_queue(args.queue, args.interval, show_elements=args.elements)
    
    else:
        print("❌ Укажите имя очереди или используйте -l для списка")
        parser.print_help()

if __name__ == "__main__":
    main()