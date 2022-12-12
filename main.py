# Подключаем приложение Flask из пакета labapp
import threading
import time

from labapp import app
from labapp import observer
from threading import Thread

"""
Этот файл запускает приложение
"""
def srv():
    app.run(host='0.0.0.0', port=8080)

def pro():
    observer.run()

if __name__ == '__main__':
    thread2 = Thread(target=srv)
    thread1 = Thread(target=pro)
    thread2.start()
    time.sleep(1)
    thread1.start()
    print("Количество потоков: %i\n" % threading.active_count())

