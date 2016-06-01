import re
import csv
import numpy as np

# функция преобразует текст в массив слов
def to_words(text):
    words = text.split()
    for i in range(len(words)):
        words[i] = words[i].strip('!,.?\(\):;\'\"\[\]-')
        words[i] = words[i].lower()
    for word in words:
        if word == '' or word == '-' or word == '\r\n':
            words.remove(word)
    return words


# функция проверяет качество статьи
def bad_text(words):
    cnt = 0
    bad_freq = 0
    latin = 0
    f = open('bad_freqs.txt', 'r', encoding='utf-8')
    bad_freqs = f.read().split()
    if len(words) > 0:
        for word in words:
            if word in bad_freqs:
                bad_freq += 1
            if re.search('[a-z]', word) is not None:
                latin += 1
        if bad_freq / len(words) >= 0.1:
            cnt += 3
        elif bad_freq / len(words) >= 0.05:
            cnt += 2
        elif bad_freq >= 1:
            cnt += 1
        if len(words) <= 8:
            cnt += 3
        elif len(words) <= 15:
            cnt += 2
        elif len(words) <= 30:
            cnt += 1
    # # 1 вариант
    #     if latin/len(words) >= 0.1:
    #         cnt += 2
    #     elif latin/len(words) >= 0.05:
    #         cnt += 1
    # 2 вариант
        if latin / len(words) >= 0.1:
            cnt += 3
        elif latin / len(words) >= 0.05:
            cnt += 2
        if cnt >= 3:
            return 1
        else:
            return 0

predict = []
really = []
with open('testarticles.txt', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        if bad_text(to_words(row[0])) != int(row[1]):
            print(bad_text(to_words(row[0])) - int(row[1]))
            print(row)
        predict.append(bad_text(to_words(row[0])))
        really.append(int(row[1]))
print("Доля неверных ответов: " + str((np.count_nonzero(np.array(predict) - np.array(really)))/len(predict)))
print("Полнота для хороших статей: " + str(((np.array(predict) + np.array(really)).tolist().count(0))/(really.count(0))))
# print("Точность для хороших статей: " + str(((np.array(predict) + np.array(really)).tolist().count(0))/(predict.count(0))))
print("Полнота для плохих статей: " + str(((np.array(predict) + np.array(really)).tolist().count(2))/(really.count(1))))
