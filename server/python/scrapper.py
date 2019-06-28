from bs4 import BeautifulSoup as bs, SoupStrainer
import requests
import sys
import json
import os
import re

# In[130]:


page = requests.get('https://boxnovel.com/novel/'+sys.argv[1])
soup = bs(page.content, 'html.parser')


# In[131]:


lastc = []
chap_dict = dict()
if (os.path.exists('../novels/'+sys.argv[1]+'.json')):
    with open('../novels/'+sys.argv[1]+'.json', 'r', encoding='utf-8') as f:
        chap_dict = json.load(f)
    for distro in chap_dict:
        lastc.append(distro)
else:
    lastc.append(' ')
# In[132]:
ulit = soup.find_all('li', class_='wp-manga-chapter')
arr = []

# In[133]:
lastc.reverse()
xd = lastc[0]
stop = 0
for x in ulit:
    if stop == 1:
        break
    for y in x.find_all('a'):
        h = y.get_text()
        if (re.search(h.strip(), xd.replace(':', ' -'))):
            stop = 1
        arr.extend([y.get_attribute_list('href') for y in x.find_all('a')][0])

# In[134]:

arr.reverse()
toupdate = []
for x in arr:
    toupdate.extend([int(s) for s in x.split('-') if s.isdigit()])

f = open('../novels/data.json','w+', encoding='utf-8')
json.dump({sys.argv[1] : ' '}, f, indent=4)

filename = '../novels/data.json'
with open(filename, 'r', encoding='utf-8') as f:
    data = json.load(f)
    data[sys.argv[1]] = "Adding Chapters"

os.remove(filename)
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

# In[135]:

tot = []
titles = []
count = 0
for c in arr:
    chap = requests.get(c)
    chapsoup = bs(chap.content, 'html.parser')
    chacont = chapsoup.div.select('.cha-words p') if chapsoup.div.select('.cha-words p') != [] else chapsoup.div.select('.reading-content p')
    chatitle = chapsoup.div.select('.cha-tit h3') if chapsoup.div.select('.cha-words p') != [] else chapsoup.div.select('.reading-content h2') if chapsoup.div.select('.reading-content h2') != [] else chapsoup.find_all('option', selected=True)
    if chatitle[0].get_text() in lastc:
        continue
    tot.append(' '.join([str(i) for i in chacont]))
    titles.append(chatitle[0].get_text())
    count += 1
    if count == 10:
        count = 0
        temp_dict = (zip(titles, tot))
        chap_dict.update(temp_dict)
        with open('../novels/'+sys.argv[1]+'.json', 'w+', encoding='utf-8') as fp:    
            json.dump(chap_dict, fp, indent=2, ensure_ascii=False)

final = dict(zip(titles, tot))
chap_dict.update(final)

with open('../novels/'+sys.argv[1]+'.json', 'w+', encoding='utf-8') as fp:    
    json.dump(chap_dict, fp, indent=2, ensure_ascii=False)


filename = '../novels/data.json'
with open(filename, 'r', encoding='utf-8') as f:
    data = json.load(f)
    data[sys.argv[1]] = "Updated"

os.remove(filename)
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print("completed!")

sys.stdout.flush()

#%%
