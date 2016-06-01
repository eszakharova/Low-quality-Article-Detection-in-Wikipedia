import re
import csv

# тестовые выборки на башкирском и мокшанском языке
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
    f = open(elem+'_bad_freqs.txt', 'r', encoding='utf-8')
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
        if len(words) <= 10:
            cnt += 3
        elif len(words) <= 20:
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

wiki = ['bawiki', 'mdfwiki']
for elem in wiki:
    good_texts = []
    bad_texts = []
    f = open(elem+'articles.txt', 'r', encoding='utf-8')
    text = f.read()
    # для быстроты пока только часть статей
    text = text[int(len(text)*7/10):int(len(text))]
    print('done reading')
    articles = re.findall('<text.*?>(.*?)</text>', text, flags=re.DOTALL)
    print('done findall')
    for article in articles:
        bad = 0
        row = []
        n2 = 0
        n3 = 0
        n4 = 0
        article = re.sub('\[\[(Файл|Няйф|Категория|Image|Category|Категорие).*?\]\]', ' ', article, flags=re.DOTALL)
        article = re.sub('{+.*?}+', ' ', article, flags=re.DOTALL)
        article = re.sub('&lt.*?gt;', ' ', article, flags=re.DOTALL)
        article = re.sub('&quot', '', article)
        article = re.sub('[\[\]]+', ' ', article)
        article = re.sub('<.*?>(?:.*?<.*?>)*', '', article, flags=re.DOTALL)
        article = re.sub('\**\s*http.*?\s', '', article, flags=re.DOTALL)
        article = re.sub('(Няйф|File|Категорие):.*?\s', '', article)
        article = re.sub('!--.*?\s', '', article)
        article = re.sub('\=\=', '', article)
        article = re.sub('\s{2,}', ' ', article)

        if re.search('[а-яёА-ЯӘәӨөҮүҠҡҒғҘҙҪҫҺһҢң]', article) is not None and re.search('return', article) is None:
            for element in to_words(article):
                if re.search('[а-яёА-ЯӘәӨөҮүҠҡҒғҘҙҪҫҺһҢң]', element) is not None:
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
                bad_texts.append(row)
            else:
                row.append(article)
                row.append(len(to_words(article)))
                row.append(bad)
                row.append(n2)
                row.append(n3)
                row.append(n4)
                row.append('good')
                good_texts.append(row)
    csvfile = open(elem + '_data.csv', 'w', encoding='utf-8')
    writer = csv.writer(csvfile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    row0 = ['Article', 'Len', 'BadFreqs', 'Len2', 'Len3', 'Len4', 'Class']
    writer.writerow(row0)
    for r in good_texts[:110]:
        writer.writerow(r)
    for l in bad_texts[:210]:
        writer.writerow(l)
    print('done all')
    print (len(good_texts))
    print (len(bad_texts))