import pandas as pd
import numpy as np
import trafilatura
import time
import random
from tqdm import tqdm

from pathlib import Path


def get_full_text_col(df: pd.DataFrame) -> None:
    """
    A method that will add a new column "full_text"
     in which the full text of the URL associated to the row will be there. It will also
     save the new DataFrame in a csv file.

    :param df: A DataFrame that contains a url column
    :return: None
    """
    full_text_list = []
    for url in tqdm(df['url']):
        try:
            content = trafilatura.fetch_url(url)
            full_text_list.append(trafilatura.extract(content,
                                                  include_comments=False,
                                                  include_tables=False,
                                                  no_fallback=False))
        except Exception as e:
            print(e)
            full_text_list.append(np.nan)
        time.sleep(random.uniform(0.1, 1))
    print("Finished")
    df['full_text'] = full_text_list
    df.to_csv('../../data/raw/raw_data_facts_full_text.csv', index=False)


if __name__ == '__main__':
    DATA_PATH = Path('../../data/raw')
    df = pd.read_csv(DATA_PATH / "raw_data_google_facts_chequeado.csv", na_values=' ')
    get_full_text_col(df)






