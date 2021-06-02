
import requests
from bs4 import BeautifulSoup

def in_stock(title, topic):
    title = title.lower()
    topic = topic.lower()
    link = 'http://books.toscrape.com/'
    topic_link = None
    r = requests.get(link)
    if r.status_code == 200:
      soup = BeautifulSoup(r.content, 'html.parser')
      nav_list = soup.find('ul', class_ = 'nav nav-list')
      topics = nav_list.find_all('a')
      for a in topics:
          b = a.text.strip().lower()
          if b == topic:
              topic_link = 'http://books.toscrape.com/'+a.get('href')
    if topic_link is not None:
        r = requests.get(topic_link)
        soup = BeautifulSoup(r.content, 'html.parser')
        #checking if there are more than one pages
        check1 = soup.find('ul', class_ = 'pager' )
        if check1 is None:
            return Booksearcher(title, topic_link)
        else:
            check2 = str(check1.find('li', class_ = 'current').text).strip()[4:].split(sep = 'of')
            start = int(check2[0])
            end = int(check2[1])
            link_part = topic_link[:-10]
            link = []
            for a in range (start, end + 1):
                link.append(link_part+'page-{}.html'.format(a))
            return Booksearcher(title, *link)
    else:
        return False

def Booksearcher(title,*pagelinks):
    title = title
    books = []
    booklist = []
    for link in pagelinks:
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'html.parser')
        books += soup.find_all('h3')
    for book in books:
        b = str(book.find('a')).split(sep='title="')
        a = b[1].split(sep='"')
        booklist.append(a[0].lower())
    if title in booklist:
        return True
    else:
        return False
