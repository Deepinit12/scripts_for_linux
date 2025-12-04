#!/bin/bash

# --- Настройки ---
DIR=/backups                   # Каталог с бэкапами
EXT="tar.gz"                   # Расширение файлов для ротации
KEEP=7                          # Количество последних файлов, которые остаются
LOG=/var/log/backup_rotate.log  # Файл для логов
DRY_RUN=1                       # 1 = только показать, 0 = удалить

# --- Проверка каталога ---
if [[ ! -d "$DIR" ]]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] Directory $DIR does not exist." | tee -a "$LOG"
    exit 1
fi

# --- Получаем список старых файлов ---
ls -1t "$DIR"/*."$EXT" 2>/dev/null | tail -n +$((KEEP + 1)) | while IFS= read -r f; do
    if [[ -z "$f" ]]; then
        continue  # если строка пустая, пропускаем
    fi

    if [[ "$DRY_RUN" -eq 1 ]]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') [DRY_RUN] Would delete: $f" | tee -a "$LOG"
    else
        if rm "$f"; then
            echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Deleted: $f" | tee -a "$LOG"
        else
            echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] Failed to delete: $f" | tee -a "$LOG"
        fi
    fi
done


