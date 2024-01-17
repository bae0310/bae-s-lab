import os

from tkinter import *
import tkinter
# from PIL import Image, ImageTk
from pygame import mixer

root = Tk()
root.attributes('-fullscreen', True)
root.title('Holocron')
root.iconphoto(False, tkinter.PhotoImage(file='SL.ico'))
root.resizable(width = False, height = False)
root['bg'] = 'grey6'

mixer.init()
mixer.Channel(0).play(mixer.Sound('Star Wars KOTOR 2 - Darth Sion (Main Menu) Theme HQ.mp3'), -1)
mixer.Channel(0).set_volume(0.8)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from tensorflow.keras.preprocessing.text import Tokenizer, text_to_word_sequence

with open('text.txt', 'r', encoding='utf-8') as g:
    texts = g.read() # считываем весь файл в одну строку
    texts = texts.replace('\ufeff', '')  # убираем первый невидимый символ

maxWordsCount = 1000 #устанавливаем макс. кол-во слов
tokenizer = Tokenizer(num_words=maxWordsCount, filters='"—#$%&amp;()*+;<=>?@[\]^`{|}~\t\n\r«»',
                      lower=False, split= '/', char_level=False) #
tokenizer.fit_on_texts([texts])
 # Топ тема. Выводит слова в порядке частоты в тексте. (слово : индекс)
# dist = list(tokenizer.word_counts.items())
# print(dist) # выводит слово и то, сколько раз оно встречается (необязательно)
data = tokenizer.texts_to_sequences([texts])# Слова в тексте превращает в последовательность чисел# Слова в тексте превращает в последовательность чисел

def solve(question):
    ans = 'неверно'
    question = question.title()
    for i in range(1, 50):
        word_indexes = tokenizer.index_word[i]
        if word_indexes in question:
            ans = tokenizer.index_word[i + 1]
            break
    if ans == 'неверно':
        ans = question[question.rfind(' ') + 1:] + '?'
        # ans = 'Я готов ответить на твой вопрос'
    return ans

def more_solve(m_question):
    mans = 'неверно'
    m_question = m_question.title()
    for i in range(1, 50):
        word_indexes = tokenizer.index_word[i]
        if word_indexes in m_question:
            mans = tokenizer.index_word[i + 2]
            break
    if mans == 'неверно':
        mans = m_question[m_question.rfind(' ') + 1:] + '?'
    return mans

def get():
    label1.delete('1.0', END)
    label1.insert(0.0, solve(e.get()))
    mixer.Channel(1).play(mixer.Sound('click_sound.mp3'))

def more_answers():
    label1.delete('1.0', END)
    label1.insert(0.0, more_solve(e.get()))
    mixer.Channel(1).play(mixer.Sound('click_sound.mp3'))

btn = Button(root,
             text = 'Получить ответ',
             command =get,
             font = ('Courier' , 20, 'italic'),
             bg = 'red4',
             fg = 'orange2',
             activebackground= 'orange',
             activeforeground= 'red')
btn.place(x = 1450, y = 1005)

button = Button(root,
                text='?',
                command=more_answers,
                width=5,
                height=2,
                font = ('Courier' , 20, 'italic'),
                bg = 'red4',
                fg = 'orange2',
                activebackground= 'orange',
                activeforeground= 'red'

                )
button.place(x = 1790, y = 970)

label1 = Text(root,
              bg='grey6', fg='yellow', font='Courier 12 italic', wrap=WORD, width=70, height=5)
label1.place(x = 10, y = 960)

# scroll = Scrollbar(command=label1.yview)
# scroll.pack(side=RIGHT, fill=Y)
# label1.config(yscrollcommand=scroll.set)

e = Entry(root, bg = 'grey6', cursor='cross' , fg= 'yellow', font='Arial 14', justify='left', width='40')
e.pack(expand=1, anchor='sw', padx=10, pady=120)

root.mainloop()