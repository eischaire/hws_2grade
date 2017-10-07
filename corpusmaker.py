import urllib.request, re, os, shutil, html

def download_page(pageUrl):
    try:
        text = ''
        page = urllib.request.urlopen(pageUrl)
        text = page.read().decode('windows-1251')
    except:
        print('Error at', pageUrl)
    return(text)

def elaborhead(text):
    head = re.sub('(</?h1>|\t|[?/\\|\*\"<>])', '', re.search('<h1>.+?</h1>', text, flags=re.DOTALL).group(), re.DOTALL)
    return(head)

def elaborcateg(text):
    categ = ''
    if re.search('news-name">.+?</div>', text, flags=re.DOTALL):
        categ = re.search('news-name">.+?</div>', text, flags=re.DOTALL).group().strip('<"news-am>/div \n').split()
    return(categ)

def clean(text):
    tags = re.compile('(<.+?>|\n\n)', re.DOTALL)
    text = html.unescape(tags.sub('', re.sub('\t', '', re.search('<div style="margin-top.+?</div>', text, re.DOTALL).group())))
    return(text)

def monthf(words):
    wordmontharr = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    nummontharr = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    for i in range(len(wordmontharr)):
        if wordmontharr[i] == words:
            words = nummontharr[i]
            break
    return(words)

def request():
    commonUrl = 'http://izvestiaur.ru/news/view/'
    tabl = open('metadata.csv', 'w', encoding='utf-8')
    for colon in ['path', 'author', 'sex', 'birthday', 'header', 'created', 'sphere', 'genre_fi', 'type', 'topic', 'chronotop', 'style', 'audience_age', 'audience_level', 'audience_size', 'source', 'publication', 'publisher', 'publ_year', 'medium', 'country', 'region']:
        tabl.write(colon)
        tabl.write('\t')
    tabl.write('language')
    tabl.write('\n')
    num = 0
    p = 0
    for i in range(120546, 122223):
        pageUrl = commonUrl + str(i) + '01' + '.html'
        text = download_page(pageUrl)
        if re.search('<div style="margin-top.+?</div>', text, re.DOTALL):
            data = re.search('article-date">.+?</div>', text, flags=re.DOTALL).group().strip('<article-dt"</v> \n').split()
            head = elaborhead(text)
            categ = elaborcateg(text)
            year = str(data[2])
            month = str(monthf(data[1]))
            data = '.'.join([data[0], monthf(data[1]), year])
            filename = str(num) + '.txt'
            k = open(filename, 'w', encoding='utf-8')
            title = '@ti ' + head
            date = '@da ' + data
            topic = '@topic ' + categ[2].lower()
            url = '@url ' + pageUrl
            for meta in ['@au NoName', title, date, topic, url]:
                k.write(str(meta))
                k.write('\n')
            k.write(clean(text))
            k.close()
            for word in clean(text).split():
                p += 1
            direct = os.path.join('IzvestiaUR', 'plain', year, month)
            if not os.path.exists(direct):
                os.makedirs(direct)
            shutil.move(os.path.join('.', filename), direct)
            num += 1
            mystemplain = os.path.join('IzvestiaUR', 'mystem-plain', year, month)
            if not os.path.exists(mystemplain):
                os.makedirs(mystemplain)
            os.system(r'mystem.exe ' + ' ' + os.path.join(direct, filename) + ' ' + os.path.join(mystemplain, filename) + ' ' + '-cid --format text')
            mystemxml = os.path.join('IzvestiaUR', 'mystem-xml', year, month)
            if not os.path.exists(mystemxml):
                os.makedirs(mystemxml)
            os.system(r'mystem.exe ' + ' ' + os.path.join(direct, filename) + ' ' + os.path.join(mystemxml, filename) + ' ' + '-idn --format xml')
            
            for inf in [os.path.join(direct, filename), '', '', '', head, data, 'публицистика', '', '', categ[2].lower(), '', 'нейтральный', 'н-возраст', 'н-уровень', 'республиканская', pageUrl, 'Известия Удмуртской Республики', '', year, 'газета', 'Россия', 'Удмуртская Республика']:
                tabl.write(str(inf))
                tabl.write('\t')
            tabl.write('ru')
            tabl.write('\n')
    tabl.close()
    shutil.move('metadata.csv', os.path.join('.', 'IzvestiaUR'))
    print(p)
    
request()
