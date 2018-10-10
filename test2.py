from urllib.request import urlopen
from bs4 import BeautifulSoup
from models.db_article import Article
import mlab
from datetime import datetime

url = 'http://genk.vn/displaymate-danh-gia-man-hinh-cua-google-pixel-3-xl-co-chat-luong-a-cao-nhat-danh-bai-ca-galaxy-note9-va-iphone-xs-max-20181010092623386.chn'
mlab.connect()

html_content = urlopen(url).read().decode('UTF-8')
soup = BeautifulSoup(html_content,'html.parser')

title = soup.find('h1', 'kbwc-title clearfix').string.replace('\r\n', '')
sapo = soup.find('h2', 'knc-sapo').string
thumbnail = (soup.find('div', 'VCSortableInPreviewMode').find('div').find('img'))['src']
contents = soup.find('div', 'knc-content').find_all('p', '')
content = ""
for i in contents:
    content = content + str(i)
author = soup.find('span', 'kbwcm-author').string
str_time = (soup.find('span', 'kbwcm-time'))['title'].replace("T", " ").replace("+07:00", "")
time = datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')

new_article = Article(
    title = title,
    sapo = sapo,
    thumbnail = thumbnail,
    content = content,
    author = author,
    time = time,
    category = "Tech"
)

new_article.save()