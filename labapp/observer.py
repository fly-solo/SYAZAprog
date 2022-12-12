import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from .models import *

class Handler(FileSystemEventHandler):
    # При любых изменениях в папке, мы перемещаем файлы в ней
    def on_modified(self, event):
        # Перебираем все файлы в папке folder_track
        for filename in os.listdir(folder_track):
            # Проверяем расширенеи файла
            extension = filename.split(".")
            # Если это поддерживаемый файл,
            if (extension[1].lower() == "txt" or extension[1].lower() == "csv"):
                # то перемещаем файл в папку
                insert_processed_data_in_DB(folder_track + filename)
                print("file " + filename + " processed")
                file = folder_track + filename
                new_path = folder_dest + extension[0] + datetime.now().strftime("%d-%m-%Y_%H-%M.") + extension[1]
                os.rename(file, new_path)


# Папка что отслеживается
folder_track = "C:/Users/gubay/PycharmProjects/SYAZAprog/labapp/source_file/"
# Папка куда перемещать будем
folder_dest = "C:/Users/gubay/PycharmProjects/SYAZAprog/labapp/processed_file/"


def run():
    # Запуск всего на отслеживание
    handle = Handler()
    observer = Observer()
    observer.schedule(handle, folder_track, recursive=True)
    observer.start()

    # Программа будет срабатывать каждые 10 милисекунд
    try:
        while (True):
             time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
