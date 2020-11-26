import pandas as pd
import requests
import time
import random
from typing import List
from datetime import datetime

"""
TOOL: https://toolbox.google.com/factcheck/explorer
API_KEY: https://support.google.com/googleapi/answer/6158862
REST_METHODS: https://developers.google.com/fact-check/tools/api/reference/rest/v1alpha1/claims/search
"""

API_KEY = 'INSERT API KEY HERE'


def get_data(resp) -> pd.DataFrame:
    if resp:
        try:
            df_outter = pd.json_normalize(resp, ['claims'], max_level=1)
            df_inner = pd.json_normalize(resp, ['claims', 'claimReview'], max_level=1)
            df_inner[['text', 'claimant', 'claimDate']] = df_outter[['text', 'claimant', 'claimDate']]
            return df_inner
        except Exception as e:
            print(e)
            return pd.DataFrame([])
    return pd.DataFrame([])


def scrape_api(terms: List[str]) -> pd.DataFrame:
    dfs = []
    lang = ['es', 'es-ES', 'es-MX', 'es-AR', 'es-CO', 'es-CL', 'es-419']
    for l in lang:
        for word in terms:
            print(f'Searching {word} in langugage {l}')
            parameters = {
                "key": API_KEY,
                'query': word,
                'languageCode': l,
                'pageSize': 10000}

            response = requests.get("https://factchecktools.googleapis.com/v1alpha1/claims:search", params=parameters)
            dfs.append(get_data(response.json()))
            time.sleep(random.uniform(10, 15))

    return pd.concat(dfs)


if __name__ == '__main__':
    to_search = ['bill gates + covid', 'bill gates covid', 'bill gates', 'dióxido covid', 'covid', 'coronavirus',
                'SARS-CoV-2', 'chile covid', 'mexico covid', 'oms', 'oms covid', 'who covid']
    df = scrape_api(to_search)
    df.drop_duplicates(inplace=True)
    df = df[df['languageCode'] == 'es']
    c_day = datetime.now().strftime('%d_%h_%Y_%H_%M')
    df.to_csv(f'../../data/raw/google_facts_api_{c_day}.csv', index=False, encoding='utf-8')
