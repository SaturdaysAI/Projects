import csv
import logging
import os
import re
from urllib.parse import urljoin

import requests
from scrapy import Selector


logger = logging.getLogger(__name__)

# Filesystem paths to gather the data.
SCRAPED_DATA_PATH = './scraped_data'
SUMMARIES_DIR = 'summaries'

# Domain where the summaries are extracted from.
SHMOOP_URL = 'https://www.shmoop.com'
SUMMARY_URL = '{url}/summary.html'

# Configuration file with the
TITLES_LIST_FILE = './config/titles_list.csv'


def get_titles_info() -> list:
    """Get the titles information from a config file."""
    with open(TITLES_LIST_FILE, 'r') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        titles_info = list(reader)

    return titles_info


def clean_text(text: str) -> str:
    """Clean a given text.

    The cleaning includes:
      - Removing special non-breaking character.
      - Removing tags.
      - Removing multiple spaces.
    """
    text = text.replace(u'\xa0', u'')
    text = re.sub('(<[^>]+>)', '', text)
    text = re.sub('[\n]+', '\n', text)
    text = re.sub('[ ]+', ' ', text)

    return text.strip()


def scrape_summaries():
    """Scrape the summaries from Shmoop website."""
    # Get the summaries to collect.
    titles_info = get_titles_info()

    # Iterate over the titles.
    for i, (_, title, url, _, _) in enumerate(titles_info):
        logger.info(f'>>> [{i}] - {title} <<<')

        # Create a directory for the title if needed.
        summary_dir = os.path.join(SCRAPED_DATA_PATH, SUMMARIES_DIR, title)
        if not os.path.exists(summary_dir):
            os.makedirs(summary_dir)

        # Parse each summary main page to extract urls for sections.
        title_summary_url = urljoin(SHMOOP_URL, SUMMARY_URL.format(url=url))
        title_summary_content = Selector(requests.get(title_summary_url))
        title_sections_urls = title_summary_content.css('.parent')[0].css('a[href]::attr(href)').getall()
        title_sections_urls = [urljoin(SHMOOP_URL, url) for url in title_sections_urls]

        if title_sections_urls:
            logging.info(f'Found {len(title_sections_urls)} sections for {title}.')
        else:
            logging.warning(f'Found no sections for {title}.')
            continue

        # Go over each section.
        for index, section_url in enumerate(title_sections_urls):
            output_filename = os.path.join(summary_dir, f'{index}.txt.utf8')
            if os.path.exists(output_filename):
                logging.info(f'Found existing section: {index}')
                continue

            # Parse section to get summary lines.
            logging.info(f'Parsing section {index}: {section_url}')
            section_content = Selector(requests.get(section_url))
            summary_content = section_content.css('div[data-element="collapse_target"]')[0]
            lines = summary_content.css('li').re('<li>(.*)</li>')
            lines = [clean_text(line) for line in lines]

            # Save the section summary lines in a file.
            with open(output_filename, 'w', encoding="utf-8") as file:
                file.writelines('\n\n'.join(lines))


if __name__ == '__main__':

    # Logging format.
    LOG_FORMAT = '%(asctime)s - %(levelname)s: %(message)s'
    LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=LOG_DATEFORMAT)

    # Execute the scraping.
    scrape_summaries()
