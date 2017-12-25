import os, re, urllib.request, time

def readpage(path):
    k = open(path, 'r', encoding='utf-8')
    text = k.read()
    return(text)

def make_arrrr():
    arrfordic = {}
    for page in os.listdir('thai_pages'):
        path = os.path.join('thai_pages', page)
        text = readpage(path)
        array = re.findall('<td class=th(.+?)td class=pos(.+?)34;(.+?)</td>', text, re.DOTALL)
        for item in array:
            partofarr = []
            for part in item:
                partofarr.append(part)
            partofarr[0] = partofarr[0].split('</td><td>')[0]
            for i, item in enumerate(partofarr):
                partofarr[i] = re.sub('<(.+?)>', '', item.strip('&#1234567890">;')).strip('</atd')
            arrfordic[partofarr[0]] = partofarr[2].split(';')[0]
    print(arrfordic)

make_arrrr()
