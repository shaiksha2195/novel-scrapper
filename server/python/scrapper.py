from bs4 import BeautifulSoup as bs, SoupStrainer
import requests
import sys
import json
import os


# In[130]:


page = requests.get('https://boxnovel.com/novel/'+sys.argv[1])
soup = bs(page.content, 'html.parser')


# In[131]:


lastc = []
if (os.path.exists('novels/'+sys.argv[1]+'.json')):
    with open('novels/'+sys.argv[1]+'.json', 'r', encoding='utf-8') as f:
        chap_dict = json.load(f)
    for distro in chap_dict:
        lastc.append(distro)


# In[132]:


ulit = soup.find_all('li', class_='wp-manga-chapter')
arr = []


# In[133]:


for x in ulit:
    arr.extend([y.get_attribute_list('href') for y in x.find_all('a')][0])


# In[134]:


arr.reverse()
toupdate = []
for x in arr:
    toupdate.extend([int(s) for s in x.split('-') if s.isdigit()])


# In[135]:


tot = []
titles = []
for c in arr:
    chap = requests.get(c)
    chapsoup = bs(chap.content, 'html.parser')
    chacont = chapsoup.div.select('.cha-words p')
    chatitle = chapsoup.div.select('.cha-tit h3')
    if chatitle[0].get_text() in lastc:
        continue
    tot.append(' '.join([str(i) for i in chacont]))
    titles.append(chatitle[0].get_text())


# In[136]:


final = dict(zip(titles,tot))
final.update(chap_dict)


# In[138]:


with open('novels/'+sys.argv[1]+'.json', 'w+', encoding='utf-8') as fp:
    json.dump(final, fp, indent=2, ensure_ascii=False)

print("completed!")

sys.stdout.flush()