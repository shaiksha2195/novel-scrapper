from bs4 import BeautifulSoup as bs, SoupStrainer
import requests
import sys
import json

page = requests.get('http://www.boxnovel.com/novel/' + sys.argv[1])
soup = bs(page.content, 'html.parser')

ulit = soup.find_all('li', class_='wp-manga-chapter')
arr = []

for x in ulit:
    arr.extend([y.get_attribute_list('href') for y in x.find_all('a')][0])

arr.reverse()
toupdate = []
for x in arr:
    toupdate.extend([int(s) for s in x.split('-') if s.isdigit()])
x = toupdate.index(int(sys.argv[2]) + 1)

tot = []
titles = []

for c in arr[x:]:
    chap = requests.get(c)
    chapsoup = bs(chap.content, 'html.parser')
    chacont = chapsoup.div.select('.cha-words p')
    chatitle = chapsoup.div.select('.cha-tit h3')
    tot.append(' '.join([str(i) for i in chacont]))
    titles.append(chatitle[0].get_text())

final = dict(zip(titles,tot))

exportfile = json.dumps({"chapters":final, "last-chap":toupdate[-1]})

print(exportfile)

sys.stdout.flush()