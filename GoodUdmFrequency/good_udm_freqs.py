import re


def to_words(text):
    words = text.split()
    for i in range(len(words)):
        words[i] = words[i].strip('!,.?\(\):;\'\"\[\]-')
        words[i] = words[i].lower()
    for word in words:
        if word == '' or word == '-' or word == '\r\n':
            words.remove(word)
    return words


f = open('good_udmarticles.txt', 'r', encoding='utf-8')
text = f.read()
all_words = to_words(text)
freq = {}
for w in range(len(all_words)):
    b = re.search('[а-яёА-ЯЁӜӝӞӟӤӥӦӧӴӵ]', all_words[w])
    if b is not None:
        d = re.search('^[0-9-]+$', all_words[w])
        if d is not None:
            all_words[w] = ''
        else:
            all_words[w] = all_words[w].lower()
            if all_words[w] not in freq and all_words[w] != '':
                freq[all_words[w]] = 1
            elif all_words[w] != '':
                freq[all_words[w]] += 1
sorted_keys = sorted(freq, key = lambda x:int(freq[x]), reverse = True)
f2 = open('good_udmfreqs.txt', 'w', encoding='utf-8')
for i in sorted_keys:
    f2.write(i+'\t'+str(freq[i])+'\n')
f2.close()