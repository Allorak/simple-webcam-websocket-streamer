# Установка
1. Склонировать репозиторий `git clone git@github.com:Allorak/simple-webcam-websocket-streamer.git`
1. Создать виртуальное окружение

**Windows**:
- `py -m venv venv`
- `.\venv\Scripts\actvate`
- `pip install -r requirements.txt`

**MacOS/Linux**:
- `python3 -m venv venv`
- `source venv/bin/actvate`
- `pip install -r requirements.txt`

3. Запустить скрипт

`python main.py`
# Работа

После запуска программы запустится вебсокет-сервер, получающий кадры с веб-камеры и преобразующий их в base64. Преобразованный кадр отправляется по вебсокетам

Сервер запускается по адресу `localhost:15555/ws`, сообщения приходят в формате `"/9j/4AAQSkZJRgABAQ...03ZP5UUVtBJgf/2Q=="`

# Настройка

В файле `main.py` можно изменить следующие параметры:
- source -- путь к входному потоку (либо id камеры, либо путь к файлу, либо путь к rtsp потоку и т д)
- host -- адрес для запуска сервера
- port -- порт для запуска сервера
- framerate для каждого события задается в конструкторе соответствующего сендера. По умолчанию для FrameSender - 15, для PeopleSender - 10.
Изменить можно например так: `PeopleSender(framerate=5)`