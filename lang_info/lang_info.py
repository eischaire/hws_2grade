import urllib.request, re, os, shutil, html
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

def collectinfo(langname):
    try:
        text = ''
        PageUrl = 'http://web-corpora.net/wsgi3/minorlangs/view/' + str(langname)
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        req = urllib.request.Request(PageUrl, headers={'User-Agent':user_agent})
        with urllib.request.urlopen(req) as response:
            text = response.read().decode('utf-8')
    except:
        print('Error at the page', PageUrl)
    return(text)

def collectcod():
    rawtext = collectinfo('overall')
    codes = []
    prelim = re.findall('wsgi3/minorlangs/view/.+?</a>', rawtext, re.DOTALL)
    for lang in prelim:
        lang = lang.split('/')[3].split('">')
        codes.append(lang[0])
    return(codes)

def makeit():
    langinf = {}
    codearr = collectcod()
    for code in codearr:
        langinf[code] = {}
        page = collectinfo(code)
        rawinf = re.findall('<tr>.+?</tr>', page, re.DOTALL)
        for item in rawinf:
            item = item.strip('</tdr>\n ').split('</td>')
            piece = item[1].split('>')
            del piece[0]
            langinf[code][str(item[0])] = html.unescape(''.join(piece))
        if re.search('<tr class="active">.+?</tr>', page, re.DOTALL):
            langinf[code]['Википедия:'] = re.search('<tr class="active">.+?</tr>', page, re.DOTALL).group().split('>')[3].split('<')[0]
### тут всё плохо и частично выдаёт не то,
### потому что формат строки "Википедия + ссылка" разнится по таблицам разных языков
###(один столбец или два), а сделать так, чтобы оно считало столбцы, я не успею
    del langinf['overall']
    return(langinf)

@app.route('/') 
def langinfo(): 
    if request.args:
        database = makeit() 
        infor = {} 
        req = request.args['language'].lower() 
        for code in database: 
            if (re.match(req, database[code]['Язык:'].lower()) or re.search(req, database[code]['Самоназвание:'].lower())): 
                for item in database[code]: 
                    infor[item] = database[code][item] 
        return render_template('answer.html', langinfo=infor) 
    return render_template('index.html') 

if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
