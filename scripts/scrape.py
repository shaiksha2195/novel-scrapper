from bs4 import BeautifulSoup as bs;

with open("index.html") as fp:
    soup = bs(fp)

soup.bs("chapter")
