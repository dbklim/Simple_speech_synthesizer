# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#       OS : GNU/Linux Ubuntu 16.04 
# COMPILER : Python 3.5.2
#   AUTHOR : Klim V. O.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

import os
import re
import threading

from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import speedup

from tkinter import Tk, Label, Text, Scrollbar, Button, END, N, S, W, E, PhotoImage
from tkinter import filedialog as fd


# Считывание .wav файлов с записями фонем
f_all_phonemes = sorted(os.listdir(path='audio'))
all_phonemes = {}
for f_phonem in f_all_phonemes:
    all_phonemes[f_phonem[:f_phonem.find('.')]] = AudioSegment.from_wav(os.path.dirname(os.path.realpath(__file__)) + '/audio/' + f_phonem)


source_text_widget = None
transcription_text_widget = None
play_thread = None


def get_phonemes(text):
    ''' Преобразует строку text в набор фонем. Возвращает строку, в которой буквы заменены на фонемы. '''
    text = text.lower()
    text = re.sub(r'\n+', '', text)
    text = re.sub(r'[^\sа-яё0-9,\.-]+', '', text)
    text = re.sub(r'0', 'ноль ', text)
    text = re.sub(r'1', 'один ', text)
    text = re.sub(r'2', 'два ', text)
    text = re.sub(r'3', 'три ', text)
    text = re.sub(r'4', 'четыре ', text)
    text = re.sub(r'5', 'пять ', text)
    text = re.sub(r'6', 'шесть ', text)
    text = re.sub(r'7', 'семь ', text)
    text = re.sub(r'8', 'восемь ', text)
    text = re.sub(r'9', 'девять ', text)
    text = re.sub(r'е', 'йэ', text)
    text = re.sub(r'ё', 'йо', text)
    text = re.sub(r'ю', 'йу', text)
    text = re.sub(r'я', 'йа', text)
    text = re.sub(r'([бвгдзклмнпрстфх])й', r"\1'", text)
    text = re.sub(r'([бвгдзклмнпрстфх])ь', r"\1'_", text)
    text = re.sub(r'([бвгдзклмнпрстфх])ъ', r'\1_', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r',', '-', text)
    text = re.sub(r'\.', '_ ', text)
    return text


def get_speech(text):
    ''' Принимает строку с фонемами и возвращает объект AudioSegment с полученной речью. '''
    phonemes = []
    i = 0
    while i < len(text):
        temp = text[i]
        if temp == "'":
            temp = text[i-1] + text[i]
            del phonemes[-1]
        i += 1
        phonemes.append(temp)

    speech = all_phonemes['_']
    for phonem in phonemes:
        speech += all_phonemes[phonem]

    speech = speech.speedup(playback_speed=1.1)
    return speech


def click_btn_load():
    f_name_source_text = fd.askopenfilename(filetypes=(("TXT файлы", "*.txt"),("Все файлы", "*.*")))
    if f_name_source_text == '':
        return

    with open(f_name_source_text, 'r') as f_source_text:
        source_text = f_source_text.read()

    global source_text_widget
    source_text_widget.delete(1.0, END)
    source_text_widget.insert(1.0, source_text)


def click_btn_transcript():
    text = source_text_widget.get(1.0, END)
    text = get_phonemes(text)

    global transcription_text_widget
    transcription_text_widget.delete(1.0, END)
    transcription_text_widget.insert(1.0, text)


def click_btn_play():
    text = source_text_widget.get(1.0, END)
    text = get_phonemes(text)

    global transcription_text_widget
    transcription_text_widget.delete(1.0, END)
    transcription_text_widget.insert(1.0, text)

    speech = get_speech(text)

    global play_thread
    if play_thread == None:
        play_thread = threading.Thread(target=lambda speech: play(speech), args=(speech,), daemon=True)
        play_thread.start()
    elif play_thread.isAlive() == False:
        play_thread = threading.Thread(target=lambda speech: play(speech), args=(speech,), daemon=True)
        play_thread.start()


def click_btn_save():
    text = source_text_widget.get(1.0, END)
    text = get_phonemes(text)

    global transcription_text_widget
    transcription_text_widget.delete(1.0, END)
    transcription_text_widget.insert(1.0, text)
    
    speech = get_speech(text)

    f_name_speech = fd.asksaveasfilename(filetypes=(("mp3 файлы", "*.mp3"),("WAV файлы", "*.wav")))
    if f_name_speech == '':
        return
    elif len(f_name_speech) == 0:
        return
    speech.export(f_name_speech, format=f_name_speech[f_name_speech.find('.')+1:])


def create_window():
    main_window = Tk()

    main_window_width = 640
    main_window_height = 305
    offset_x = int(main_window.winfo_screenwidth()/2 - main_window_width/2)
    offset_y = int(main_window.winfo_screenheight()/2 - main_window_height/2)

    main_window.title('Простой синтезатор речи')
    main_window.geometry(str(main_window_width)+'x'+str(main_window_height)+'+'+str(offset_x)+'+'+str(offset_y))
    main_window.resizable(width=False, height=False)
    main_window.tk.call('wm', 'iconphoto', main_window._w, PhotoImage(file='icon.gif'))

    source_text_label = Label(text='Исходный текст:')
    source_text_label.grid(row=1, column=1, sticky=W)
 
    transcription_label = Label(text='Транскрипция:')
    transcription_label.grid(row=4, column=1, sticky=W)

    global source_text_widget
    source_text_widget = Text(width=60, height=9)
    source_text_widget.grid(row=2, column=1, rowspan=2)

    scroll_source_text = Scrollbar(command=source_text_widget.yview)
    scroll_source_text.grid(row=2, column=2, rowspan=2, sticky=N+S+W)

    source_text_widget.config(yscrollcommand=scroll_source_text.set)

    global transcription_text_widget
    transcription_text_widget = Text(width=60, height=9)
    transcription_text_widget.grid(row=5, column=1, rowspan=2)

    scroll_transcription_text = Scrollbar(command=transcription_text_widget.yview)
    scroll_transcription_text.grid(row=5, column=2, rowspan=2, sticky=N+S+W)

    transcription_text_widget.config(yscrollcommand=scroll_transcription_text.set)


    btn_load = Button(text='Загрузить из файла', background='#555', foreground='#ccc', width=20, command=click_btn_load)
    btn_load.grid(row=2, column=3, padx=10, pady=15)

    btn_transcript = Button(text='Получить транскрипцию', background='#555', foreground='#ccc', width=20, command=click_btn_transcript)
    btn_transcript.grid(row=3, column=3, padx=10, pady=15)

    btn_play = Button(text='Воспроизвести', background='#555', foreground='#ccc', width=20, command=click_btn_play)
    btn_play.grid(row=5, column=3, padx=10, pady=15)

    btn_save = Button(text='Сохранить в файл', background='#555', foreground='#ccc', width=20, command=click_btn_save)
    btn_save.grid(row=6, column=3, padx=10, pady=15)

    return main_window


if __name__ == '__main__':
    main_window = create_window()
    main_window.mainloop()