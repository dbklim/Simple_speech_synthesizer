# Simple_speech_synthesizer
Простой синтезатор русской речи. Преобразует входной текст в набор фонем, а затем путём сопоставления каждой фонемы и её аудиозаписи синтезируется речь. Для запуска выполните `run.sh` или `python3 speech_synthesizer.py`.

Полный список всех необходимых для работы пакетов:
  1. Для Python3.5: tkinter, pydub, simpleaudio.
  2. Для Ubuntu: python3.5-dev, python3-pip, python3-tk, ffmpeg, libavcodec-extra.

Если вы используете Ubuntu 16.04 или выше, для установки всех пакетов можно воспользоваться `install_packages.sh` (проверено в Ubuntu 16.04).
