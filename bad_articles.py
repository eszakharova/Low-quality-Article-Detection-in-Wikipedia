import re
import csv


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
    global bad
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
        bad = bad_freq
        if cnt >= 3:
            return 1
        else:
            return 0


f = open('udmarticles.txt', 'r', encoding='utf-8')
text = f.read()
# для быстроты пока только часть статей
text = text[int(len(text)*5/10):int(len(text))]
print('done reading')
articles = re.findall('<text.*?>(.*?)</text>', text, flags=re.DOTALL)
# # если вдруг понадобятся названия статей
# titles = re.findall('(<title>.*?</title>).*?<text.*?>.*?</text>', text, flags=re.DOTALL)
print('done findall')

csvfile = open('article_data.csv', 'w', encoding='utf-8')
writer = csv.writer(csvfile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
# bad = open('bad.txt', 'w', encoding='utf-8')
# good = open('good.txt', 'w', encoding='utf-8')
row0 = ['Article', 'Len', 'BadFreqs', 'Len2', 'Len3', 'Len4', 'Class']
writer.writerow(row0)
for article in articles:
    bad = 0
    row = []
    n2 = 0
    n3 = 0
    n4 = 0
    article = re.sub('\[\[(Файл|Суред|Категория|Image|Category).*?\]\]', ' ', article, flags=re.DOTALL)
    # article = re.sub('\|.*?[\|;]', ' ', article)
    article = re.sub('{+.*?}+', ' ', article, flags=re.DOTALL)
    article = re.sub('&lt.*?gt;', ' ', article, flags=re.DOTALL)
    article = re.sub('&quot', '', article)
    article = re.sub('[\[\]]+', ' ', article)
    article = re.sub('<.*?>(?:.*?<.*?>)*', '', article, flags=re.DOTALL)
    article = re.sub('\**\s*http.*?\s', '', article, flags=re.DOTALL)
    article = re.sub('(Суред|File):.*?\s', '', article)
    article = re.sub('!--.*?\s', '', article)
    article = re.sub('\=\=', '', article)
    article = re.sub('\s{2,}', ' ', article)

    if re.search('[а-яёА-Я]', article) is not None:
        for element in to_words(article):
            if re.search('[а-яёА-Я]', element) is not None:
                if len(element) == 2:
                    n2 += 1
                elif len(element) == 3:
                    n3 += 1
                elif len(element) == 4:
                    n4 += 1

        if bad_text(to_words(article)) == 1:
            row.append(article)
            row.append(len(to_words(article)))
            row.append(bad)
            row.append(n2)
            row.append(n3)
            row.append(n4)
            row.append('bad')
            # print('bad bad bad')
            # bad.write(article + '@' + '\n')  # @ в роли разделителя

        else:
            row.append(article)
            row.append(len(to_words(article)))
            row.append(bad)

            row.append(n2)
            row.append(n3)
            row.append(n4)
            row.append('good')
            # print('good good good')
            # good.write(article + '@' + '\n')

        writer.writerow(row)

# bad.close()
# good.close()

print('done all')
