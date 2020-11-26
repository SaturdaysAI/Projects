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
    news = r.html.find('div.ws-search-components', first=True)
    pagination = r.html.find('.ws-search-pagination', first=True)
    pages = news.absolute_links.difference(pagination.absolute_links)
    next_page = list(r.html.find('a.next', first=True).links)[0]
    return pages, 'https://www.bbc.com/mundo/search' + next_page


def scrape_page(url: str) -> None:
    """
    A method that will be scrape the articles of a given url and save it as a csv file.
    Particularly from 'https://www.bbc.com/mundo/search?q=<TERM_TO_SEARCH>'
    :param url: The url of the search engine
    :return: None
    """
    term_to_search = url.split('=')[-1]
    s = HTMLSession()
    # # First search
    articles_pages, next_page = get_articles_pages(url, s)
    idx = 1

    with open(f'../../data/raw/bbc_articles_{term_to_search}.csv', 'w', newline='') as csvfile:
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
    url = 'https://www.bbc.com/mundo/search?q=covid'
    scrape_page(url)

