import os
import shutil
import datetime
import requests
import sys

# --- НАСТРОЙКИ ---
# Папка, которую мы хотим забэкапить (например, сохранения игры)
SOURCE_DIR = "test_data" 
# Папка, куда будем складывать архивы
BACKUP_DIR = "backups"
# Твой Discord Webhook URL (мы получим его на следующем шаге)
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1566969177497931936/cCQkqC1pAMS3SfxFxA11cl-GkzFlSAMfXiX5Cv7MqL4ObX8OYPpfSHqH4xyrMbbT38vL"

def create_backup():
    # 1. Проверяем, существует ли исходная папка
    if not os.path.exists(SOURCE_DIR):
        print(f"Ошибка: Папка {SOURCE_DIR} не найдена.")
        return None

    # 2. Создаем папку для бэкапов, если ее нет
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    # 3. Формируем имя архива с текущей датой и временем
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archive_name = f"backup_{timestamp}"
    
    # 4. Создаем zip-архив
    try:
        print(f"Создаю архив: {archive_name}...")
        shutil.make_archive(os.path.join(BACKUP_DIR, archive_name), 'zip', SOURCE_DIR)
        print("Архив успешно создан!")
        return archive_name
    except Exception as e:
        print(f"Ошибка при создании архива: {e}")
        return None

def send_discord_notification(archive_name):
    if not DISCORD_WEBHOOK_URL or DISCORD_WEBHOOK_URL == "ТВОЙ_URL_ЗДЕСЬ":
        print("Discord Webhook URL не настроен. Пропускаю уведомление.")
        return

    # Формируем сообщение
    message = {
        "content": f"✅ **Бэкап успешно создан!**\n📁 Файл: `{archive_name}.zip`"
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=message)
        response.raise_for_status()
        print("Уведомление в Discord отправлено.")
    except Exception as e:
        print(f"Ошибка при отправке в Discord: {e}")

if __name__ == "__main__":
    print("--- Запуск скрипта бэкапа ---")
    archive_name = create_backup()
    if archive_name:
        send_discord_notification(archive_name)
    else:
        print("Бэкап не был создан, уведомление не отправлено.")
