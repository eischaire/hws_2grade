from flask import Flask, render_template, request, url_for
import re, json

k = open('database.csv', 'a', encoding='utf-8')
tablecap = 'Респондент' + '\t' + 'Пол' + '\t' + 'Возраст' + '\t' + 'Город' + '\t' + 'Образование' + '\t' + 'Ленина' + '\t' 'Гороховая' + '\t' + 'Столярный' + '\t' + 'Верхняя' + '\t' + 'Западный' + '\t' + 'Черепичный' + '\t' + 'Невский' + '\t' + 'Красный' + '\t' + '35' + '\n'
k.write(tablecap)
app = Flask(__name__)

@app.route('/')
def fillin():
    if request.args:
        name = request.args['name']
        region = request.args['region']
        sex = request.args['sex']
        edu = request.args['edu']
        age = request.args['age']
        persinf = {}
        persinf['name'] = name
        persinf['region'] = region
        persinf['sex'] = sex
        persinf['edu'] = edu
        persinf['age'] = age
        streetans = {}
        for item in request.args.keys():
            if item not in persinf.keys():
                streetans[item] = request.args[item]
        strarr = []
        for ans in streetans.values():
            strarr.append(ans)
        strstr = '\t'.join(strarr) + '\n'
        tablerow = name + '\t' + sex + '\t' + age + '\t' + region + '\t' + edu + '\t' + strstr
        k.write(tablerow)
        k.close()
        return render_template('answer.html', name = name, age = age, sex = sex, edu = edu, region = region)
    return render_template('form.html') 

def collectstat(filename):
    stats_arr = []
    k = open(filename, 'r', encoding='utf-8')
    resp_arr = k.readlines()
    for i in range(len(resp_arr)):
        if not resp_arr[i] == tablecap:
            stats_arr.append(resp_arr[i].split('\t'))
    name = []
    sex = []
    age = []
    city = []
    edu = []
    lenin = []
    goroh = []
    stol = []
    verh = []
    west = []
    cher = []
    nevs = []
    red = []
    ciph = []
    stat = [name, sex, age, city, edu, lenin, goroh, stol, verh, west, cher, nevs, red, ciph]
    
    for statrow in stats_arr:
        for j in range(len(statrow)):
            stat[j].append(statrow[j])
    return stat

@app.route('/stats')
def stats():
    stat = collectstat('database.csv')
    statdic = []
    for a, crit in enumerate(stat):
        dic = {}
        crit = crit
        for t, incid in enumerate(crit):
            if incid not in dic:
                dic[incid] = 1
            else:
                dic[incid] += 1
        statdic.append(dic)
    
    return render_template('stats.html', statdic = statdic)


@app.route('/json')
def makejson():
    json_str = json.dumps(collectstat('database.csv'), ensure_ascii = False)
    return render_template('json.html', json_str = json_str)

@app.route('/results')


@app.route('/search')
def search():
    req_arr = []
    if request.args:
        region = request.args['region']
        sex = request.args['sex']
        age = request.args['age']
        k = open('database.csv', 'r', encoding='utf-8')
        for line in k.readlines():
            check = []
            for item in [region, sex, age]:
                if not len(item) == 0:
                    check.append(item)
                    num = 0
                    for item2 in check:
                        if re.search(item2, line):
                            num += 1
                    if num == len(check):
                        req_arr.append(line.split('\t'))
        return render_template('results.html', req_arr = req_arr)
    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)

k.close()
