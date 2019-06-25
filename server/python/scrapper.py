from bs4 import BeautifulSoup as bs, SoupStrainer
import requests
import sys
import json

page = requests.get(sys.argv[1])
soup = bs(page.content, 'html.parser')

ulit = soup.find_all('li', class_='wp-manga-chapter')
arr = []

for x in ulit:
    arr.extend([y.get_attribute_list('href') for y in x.find_all('a')][0])

arr.reverse()
tot = []
titles = []

for c in arr[0:2]:
    chap = requests.get(c)
    chapsoup = bs(chap.content, 'html.parser')
    chacont = chapsoup.div.select('.cha-words p')
    chatitle = chapsoup.div.select('.cha-tit h3')
    tot.append(str(chacont))
    titles.append(chatitle[0].get_text())

final = dict(zip(titles,tot))

exportfile = json.dumps(final)

f= open(sys.argv[1][27:-1]+'.json',"w+")

f.write(exportfile)

f.close