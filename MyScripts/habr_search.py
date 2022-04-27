import requests
from bs4 import BeautifulSoup
import fake_useragent

key_words = ['чудо', 'html', 'web', 'python']
max_key_len = max([len(length) for length in key_words]) # For beautifying printout

class HabrSearch:
    base_url = 'https://habr.com'
    all_ru_url = 'https://habr.com/ru/all'
    habr_ua = fake_useragent.UserAgent()
    header = {'User-Agent': str(habr_ua.chrome)}
    result_count = 0

    def paginator(self):
        """
        Получает первую страницу для анализа, затем итерирует по следующим получая next_page
        """
        request = requests.get(self.all_ru_url, headers=self.header)
        soup = BeautifulSoup(request.text, 'html.parser')
        self._search_page(soup)
        while True:
            try:
                next_page = self.base_url + soup.find(id='pagination-next-page')['href']
            except KeyError:
                print('All articles gathered!')
                return
            request = requests.get(next_page, headers=self.header)
            soup = BeautifulSoup(request.text, 'html.parser')
            self._search_page(soup)

    def _search_page(self, soup):
        """
        Либо получает и анализирует статьи на странице,
        либо получет ссылку на каждую статью и анализирует отдельно в _analyze_article.
        "Звуковые статьи" исключаются.
        Отдельная обработка "мега" статей.
        """
        page_soup = soup.find(class_='tm-articles-subpage').find_all('article')
        for article in page_soup:
            if 'tm-voice-article' in article['class']:
                continue

# """Основное задание, строки 45-56"""
#             if 'tm-megapost-snippet' in article.div['class']:
#                 preview = article.find(class_='article-formatted-body_version-1')
#                 date = article.find('time')['title']
#                 head = article.find('h2').text
#                 link = self.base_url + article.find(class_='tm-megapost-snippet__date')['href']
#             else:
#                 preview = article.find(class_='tm-article-body tm-article-snippet__lead')
#                 date = article.find('time')['title']
#                 head = article.find('h2').text
#                 link = self.base_url + article.find('h2').a['href']
#
#             self._match_print(preview, date, head, link)

# """дополнительное задание по анализу внутри статьи, строки 59-63 + метод _analyze_article"""
            if 'tm-megapost-snippet' in article.div['class']:
                a_link = self.base_url + article.find(class_='tm-megapost-snippet__date')['href']
            else:
                a_link = self.base_url + article.find('h2').a['href']
            self._analyze_article(a_link)

    def _analyze_article(self, link):
        """
        Анализирует отдельную статью
        """
        a_request = requests.get(link, headers=self.header)
        a_soup = BeautifulSoup(a_request.text, 'html.parser')
        a_body = a_soup.find(id='post-content-body')
        date = a_soup.find(class_='tm-article-snippet__datetime-published').time['title']
        head = a_soup.find(class_='tm-article-presenter__snippet').find('h1').text
        self._match_print(a_body, date, head, link)

    def _match_print(self, body, date, head, link):
        """
        Вызывается для печати при совпадении ключевых слов
        """
        for word in key_words:
            if word in body.text:
                self.result_count += 1
                print(f'Совпадение по {word:<{max_key_len}} - {date} - {head} - {link}')
                break
