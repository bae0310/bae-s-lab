import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np

from tensorflow.keras.layers import Dense, SimpleRNN, Input, Embedding
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer, text_to_word_sequence
from tensorflow.keras.utils import to_categorical


with open('answers.txt', 'r', encoding='utf-8') as f:
    texts = f.read() # считываем весь файл в одну строку
    texts = texts.replace('\ufeff', '')  # убираем первый невидимый символ



maxWordsCount = 1000 #устанавливаем макс. кол-во слов
tokenizer = Tokenizer(num_words=maxWordsCount, filters='"—#$%&amp;()*+;<=>?@[\]^`{|}~\t\n\r«»',
                      lower=True, split= ' ', char_level=False) #


tokenizer.fit_on_texts([texts])

word_indexes = tokenizer.word_index
print(word_indexes) # Топ тема. Выводит слова в порядке частоты в тексте. (слово : индекс)

# dist = list(tokenizer.word_counts.items())
# print(dist) # выводит слово и то, сколько раз оно встречается (необязательно)

data = tokenizer.texts_to_sequences([texts])# Слова в тексте превращает в последовательность чисел
print(data)

# for i in range(len(data[0])):
#     i += 1
# print(i)
#res = to_categorical(data[0], num_classes=maxWordsCount) Это не надо, видимо

# Каждое значение превращаем в вектор, состоящий из 1 и 0. Например [3] = [0, 0, 1] (при num_classes = 3). Если num_classes = 5, то будет [0, 0, 1, 0, 0]. Это кол-во столбцов в матрице!!!!!

res = np.array(data[0])
print(res.shape) #Выведет (i,)


inp_words = 2
n = res.shape[0] - inp_words


X = np.array([res[i:i + inp_words] for i in range(n)])
# Че здесь написано: Делаем массив (array) из списка1. Список1 состоит из элементов списка res. Эти элементы мы перебираем так: [1:4] (с 1-ого по 3-ий), [2:5], [3:6] и так далее


Y = to_categorical(res[inp_words:], num_classes=maxWordsCount)# Каждое значение превращаем в вектор 1 и 0. Y -- это выходные значения

model = Sequential()
model.add(Embedding(maxWordsCount, 256, input_length = inp_words))
#Embedding(input_dim(размер словаря, по идеи maxWordsCount), output_dim, input_length=None)
model.add(SimpleRNN(128, activation='relu'))
model.add(Dense(maxWordsCount, activation='softmax'))
model.summary()

model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

history = model.fit(X, Y, batch_size=32, epochs=30)


def buildPhrase(texts, str_len=50):
    res = texts

    data = tokenizer.texts_to_sequences([texts])[0]# Опять разбиваем НАБРАННЫЙ текст на числа. В конце поставить [0]
    for i in range(str_len):# предсказывать слова будет 50 раз
        # x = to_categorical(data[i: i + inp_words], num_classes=maxWordsCount)  # преобразуем в One-Hot-encoding
        # inp = x.reshape(1, inp_words, maxWordsCount)
        x = data[i: i + inp_words] # Создаем вектор, который состоит
        inp = np.expand_dims(x, axis=0)

        pred = model.predict(inp) # Это вектор, состоящий из maxWordsCount элементов
        indx = pred.argmax(axis=1)[0] # Берем индекс того элемента, который принимает макс значение
         # Останавливаемся на слэше
        data.append(indx) # Добавляем его в

        res += " " + tokenizer.index_word[indx]  # преобразуем в слово
    return res
#
# def solve(question):
#     ans = 'неверно'
#     question =question.title()
#     for i in range(1, 50):
#         word_indexes = tokenizer.index_word[i]
#         if word_indexes in question:
#             ans = tokenizer.index_word[i + 1]
#             break
#     return ans
# u_input = 1
# while u_input != 'достаточно от тебя уроков':
#     u_input = input('Я готов ответить на твой вопрос:')
#     print(solve(u_input))
user_input = 'Меня зовут Дарт Р..., темный владыка ситов.\nЯ являюсь наследником династии зла Дарта Бейна.\nЯ передам тебе свои знания о темной стороне Силы. '
print(user_input)
while user_input != 'достаточно от тебя уроков':
    user_input = input('Я готов ответить на твой вопрос:')
    if user_input == 'достаточно от тебя уроков':
        break
    res = buildPhrase(user_input)
    print(res)
