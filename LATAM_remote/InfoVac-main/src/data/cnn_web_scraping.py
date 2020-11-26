import csv
import trafilatura
import time
import random

from typing import List, Tuple
from requests_html import HTMLSession


def get_articles_pages(url: str, s: HTMLSession) -> Tuple[List[str], str]:
    """ Method that given a url of the results of a search page will get
        the urls of the results.

    :param url: url that have the results of a search
    :param s: HTML Session for request content
    :return: a tuple containing a list of links and the next link of the pagination
    """

    r = s.get(url, timeout=60)
    print("STATUS_CODE:", r.status_code)
    news = r.html.xpath('//*[@id="content"]/div[2]/div/div[2]', first=True)
    pagination = r.html.find('div.search__wrappagination', first=True)
    pages = news.absolute_links.difference(pagination.absolute_links)
    next_page = r.html.find('a.next', first=True)
    return filter_pages(pages), list(next_page.absolute_links)[0]


def filter_pages(links: List[str]) -> List[str]:
    """ Method to remove video, category, seccion and gallery pages

    :param links: List of links which will be filtered
    :return: List of links filtered, without video, category, seccion and gallery pages
    """

    dropped = ['video', 'category', 'seccion', 'gallery']
    return [page for page in links if page.split('/')[3] not in dropped]


def scrape_page(url: str) -> None:
    """
    A method that will be scrape the articles of a given url and save it as a csv file.
    Particularly from 'https://cnnespanol.cnn.com/?s=<TERM_TO_SEARCH>'
    :param url: The url of the search engine
    :return: None
    """
    term_to_search = url.split('=')[-1]
    s = HTMLSession()
    # # First search
    articles_pages, next_page = get_articles_pages(url, s)
    idx = 1

    with open(f'../../data/raw/cnn_articles_{term_to_search}.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'url', 'author', 'date', 'description', 'sitename', 'title', 'text', 'categoria']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        while next_page:
            for page in articles_pages:
                print(f'url:', page)
                time.sleep(random.uniform(1, 2))
                try:
                    content = trafilatura.fetch_url(page)
                    article = trafilatura.metadata.extract_metadata(content)
                    article['text'] = trafilatura.extract(content, include_comments=False,
                                                          include_tables=False,
                                                          no_fallback=False)

                    writer.writerow({'id': idx,
                                     'url': article['url'],
                                     'author': article['author'],
                                     'date': article['date'],
                                     'description': article['description'],
                                     'sitename': article['sitename'],
                                     'title': article['title'],
                                     'text': article['text'],
                                     'categoria': 'confiable'})

                except Exception as e:
                    print("Failed to get content", e)
                idx += 1
            print('=' * 50)
            print("NEXT:", next_page)
            try:
                articles_pages, next_page = get_articles_pages(next_page, s)
            except Exception as e:
                print("Failed to get new search page", e)
            time.sleep(random.uniform(10, 15))
    print("Finished")


if __name__ == '__main__':
    url = 'https://cnnespanol.cnn.com/?s=coronavirus'
    scrape_page(url)



