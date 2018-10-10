from urllib.request import urlopen
from bs4 import BeautifulSoup
from models.db_article import Article
import mlab
from datetime import datetime

url = 'http://bongdanet.vn/hau-truong-san-co/nhung-vu-mua-ban-dam-noi-tieng-trong-lang-bong-da-the-gioi-tbd71819'
mlab.connect()

html_content = urlopen(url).read().decode('UTF-8')
soup = BeautifulSoup(html_content, 'html.parser')

info = soup.find('div', 'article-text-info')
meta = info.find('meta', itemprop = 'author')
meta2 = info.find('meta', itemprop = "datePublished")
times = meta2['content']
times1 = times.replace("T", " ").replace("+07:00", "")
time = datetime.strptime(times1, '%Y-%m-%d %H:%M:%S')
img = soup.find("img", "img-detail-news")
body = soup.find ('div', 'article-body')
contents = body.find_all('p')
content = ""
for i in contents:
    content = content + str(i)

new_article = Article(
    title = soup.find("h1", 'title-news').string,
    sapo = soup.find("p", 'content-brief').string,
    thumbnail = img['src'],
    content = content,
    author = meta['content'],
    time = meta2['content'],
)

new_article.save()