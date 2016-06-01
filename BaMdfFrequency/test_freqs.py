import xml.dom.minidom
import re
wiki = ['bawiki', 'mdfwiki']
for elem in wiki:
    f = open(elem+'.xml', 'r', encoding = 'utf-8')
    text = xml.dom.minidom.parse(f)
    text = text.toprettyxml()
    pages = re.findall('<page>.*?</page>', text, flags = re.DOTALL)
    f1 = open(elem+'articles.txt', 'w', encoding = 'utf-8')
    for page in pages:
        f1.write(page + '\n')
    f1.close()
    text = re.sub('(<(?:sitename|namespaces|comment)+>.*?<(?:/sitename|/namespaces|/comment)+>)', '', text, flags = re.DOTALL)
    text = re.sub('(\[\[:*(?:Категория|Category).*?\]\])', '', text, flags = re.DOTALL)
    text = re.sub('\[\[(Файл|файл|:Категория|Шаблон|Википедия)', '', text)
    text = re.sub('#перенаправление', '', text )
    text = re.sub('[\[\]]+', '', text)
    words = re.findall('([а-яёА-ЯЁӘәӨөҮүҠҡҒғҘҙҪҫҺһҢң0-9]+-*[а-яёА-ЯЁӘәӨөҮүҠҡҒғҘҙҪҫҺһҢң]*)', text)
    freq = {}
    for w in range(len(words)):
        d = re.search('^[0-9-]+$', words[w])
        if d is not None:
            words[w] = ''
        else:
            words[w] = words[w].lower()
            if words[w] not in freq and words[w] != '':
                freq[words[w]] = 1
            elif words[w] != '':
                freq[words[w]] += 1
    sorted_keys = sorted(freq, key = lambda x:int(freq[x]), reverse = True)
    f2 = open(elem+'freqs.txt', 'w', encoding='utf-8')
    for i in sorted_keys:
        f2.write(i+'\t'+str(freq[i])+'\n')
    f2.close()
