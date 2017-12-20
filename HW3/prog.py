import os, json, re, urllib.request, html
from pymystem3 import Mystem
from flask import Flask, render_template, request

def download_page(pageUrl):
    try:
        text = ''
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        req = urllib.request.Request(pageUrl, headers={'User-Agent': user_agent})
        with urllib.request.urlopen(req) as page:
            text = page.read().decode('utf-8')
        print('everything is ok')
    except:
        print('Error at', pageUrl)
    return(text)

mystem = Mystem()

def sub_change(form, lemma, stem):
    frmdc = {}
    lmmdc = {}
    stmdc = {}
    n_lmmdc = {}
    flx = {}
    for i, letter in enumerate(form):
        frmdc[i] = letter
    print('frmdc: ',frmdc)
    for j, letter in enumerate(lemma):
        lmmdc[j] = letter
    print('lmmdc: ',lmmdc)
    for k, letter in enumerate(stem):
        stmdc[k] = letter
    print('stmdc: ',stmdc)
    for i in frmdc:
        if not i in lmmdc or lmmdc[i] != frmdc[i]:
            flx[i] = frmdc[i]
    print(flx)
    for i in stmdc:
        if not i in lmmdc or lmmdc[i] != stmdc[i]:
            n_lmmdc[i] = stmdc[i]
        else:
            n_lmmdc[i] = lmmdc[i]
    print(n_lmmdc)
    for i in flx:
        if not i in n_lmmdc or n_lmmdc[i] != flx[i]:
            n_lmmdc[i] = flx[i]
    if n_lmmdc[len(n_lmmdc) - 1] == 'е' and not re.search('им', str(mystem.analyze(form.strip('\n'))[0]['analysis'][0])) and not re.search('вин', str(mystem.analyze(form.strip('\n'))[0]['analysis'][0])) :
        n_lmmdc[len(n_lmmdc) - 1] = 'ѣ'
    result = ''
    for i in n_lmmdc:
        result = result + n_lmmdc[i]
    return(result)

    
def forms(form, pos, lemma, stem):
    print(form, lemma, stem, sep=', ')
    if pos == 'S':
        result = sub_change(form, lemma, stem)
    if pos == 'V':
        result = v_change(form, lemma, stem)
    if pos == 'SPRO':
        result = spro_change(form, lemma, stem)
    if pos == 'APRO' or pos == 'A' or pos == 'ANUM':
        result = adj_change(form, lemma, stem)
    if pos == 'NUM':
        result = num_change(form, lemma, stem)
    voc = 'аоуэыяёюеиъѣь'
    k = 0
    for i in range(len(voc)):
        if not result.endswith(voc[i]):
            k += 1
    if k == len(voc):
        result = result + 'ъ'
    return(result)


def makereq(word, pos, init, lemma):
    req_line = 'http://slovnik.narod.ru/old/slovar/{0}.html'.format(init)
    text = download_page(req_line)
    reqword = '<td>{0}</td>\n'.format(lemma)
    needed = ''
    finwrd = ''
    if re.search(reqword, text, re.DOTALL):
        needed = html.unescape(re.search('<td>{0}</td>\n +?<td>(.+?)</td>'.format(lemma), text, re.DOTALL).group())
        finwrd = html.unescape(re.sub('<td>{0}</td>\n +?<td>(.+?)</td>'.format(lemma), '\\1', needed)).split(',')[0]
        RESULT = forms(word, pos, lemma, finwrd)
    else:
        word = word.split()
        for i in range(len(word) - 1):
            if word[i] == 'и' and word[i+1] in 'аоуэыяёюеи':
                word[i] = 'i'
        RESULT = ''.join(word)
    return(RESULT)

def stemming(word):
    print(mystem.analyze(word))
    parsed = mystem.analyze(word.strip('\n'))[0]['analysis'][0]
    pos = mystem.analyze(word.strip('\n'))[0]['analysis'][0]['gr'].split(',')[0]
    lemma = str(parsed['lex'])
    diclet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'sch', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'x', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'э': 'ya', 'ю': 'ya', 'я': 'ya'}
    for let in diclet:
        if lemma.startswith(let):
            init = diclet[let]
            break
    if lemma.startswith('по'):
        init = 'po'
    p_arr = ['пр', 'пс', 'пт', 'пу', 'пф', 'пх', 'пц', 'пч', 'пш', 'пщ', 'пъ', 'пы', 'пь', 'пэ', 'пю', 'пя']
    for p in p_arr:
        if lemma.startswith(p):
            init = 'pr'
            break
    s_arr = ['см', 'сн', 'со', 'сп', 'ср', 'сс', 'ст', 'су', 'сф', 'сх', 'сц', 'сч', 'сш', 'сщ', 'съ', 'сы', 'сь', 'сэ', 'сю']
    for s in s_arr:
        if lemma.startswith(s):
            init = 'sm'
            break
    result = makereq(word, pos, init, lemma)
    return(result)

app = Flask(__name__)

@app.route('/')
def inputwrd():
    result = ''
    if request.args:
        word = request.args['word']
        if len(word) == 0:
            result = 'ERROR TRY ANOTHER'
        else:
            result = stemming(word)
        return render_template('results.html', word = word, result = result)
    return render_template('index.html')

@app.route('/test')
def anssheet():
    if request.args:
        devil = request.args['devil']
        runaway = request.args['runaway']
        sea = request.args['sea']
        battery = request.args['battery']
        envelop = request.args['envelop']
        white = request.args['white']
        creme = request.args['creme']
        water = request.args['water']
        me = request.args['me']
        everyone = request.args['everyone']
        fort = request.args['fort']
        return render_template('answers.html', x_arr = request.args.values())
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)
