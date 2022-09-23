import math
import os

import numpy as np
import pandas as pd
import tqdm
from tqdm import tqdm
from transformers import (
    pipeline,
    AutoTokenizer,
    TFAutoModelForSeq2SeqLM,
)


tqdm.pandas()

MODELS_DIR = "./models"


def load_model(summarizer_path: str, tokenizer_path: str):
    """Load the trained summarizer model and tokenizer.

    Both models, the summarizer and the tokenizer were trained
    with our data.
    """
    summarizer = TFAutoModelForSeq2SeqLM.from_pretrained(summarizer_path)
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    return summarizer, tokenizer


def create_summarization_pipeline():
    """Create a pipeline based on our model and tokenizer."""
    train_model_path = os.path.join(MODELS_DIR, 'train_model')
    tokenizer_path = os.path.join(MODELS_DIR, 'train_tokenizer')
    model, tokenizer = load_model(train_model_path, tokenizer_path)
    return pipeline('summarization', model=model, tokenizer=tokenizer)


def load_tale(tale_path: str) -> tuple[str, pd.DataFrame]:
    """Load a tale from the given file.

    Load the tale in .txt format and add index it for
    later grouping.
    """
    with open(tale_path, 'r') as f:
        # Read the .txt file.
        lines = f.readlines()

        # Title is the first line of the file.
        title = lines[0]

        # Each paragraph is a row of DataFrame.
        tale = pd.DataFrame({'story': lines[1:]})
        tale = tale[tale.story != '\n'].reset_index()

        return title, tale


def reduce_tale(tale: pd.DataFrame, num: int) -> pd.DataFrame:
    """Reduce the length of the tale for summarization.

    Add index column to a tale for merge. The index column
    looks like: ['0', '0', '0', '1', '1', '1'...].
    """
    # Number of rows the DataFrame will have after merging.
    rows = math.ceil(int(len(tale)) / num)

    # Create a list of index and add it as a new column.
    index_list = []
    for i_row in range(rows):
        n = [str(i_row)] * num
        index_list = index_list + n

    tale['index'] = np.array(index_list)[:len(tale)]

    return tale


def prepare_tale(tale: pd.DataFrame) -> pd.DataFrame:
    """Prepare tale for summarization."""
    # Create a new DataFrame.
    prepared_tale = pd.DataFrame(columns=['story', 'summ'])

    # Merge rows by index to reduce length of df
    prepared_tale['story'] = tale.groupby(['index'])['story'].apply('/n/n'.join)

    # Quick clean the story.
    prepared_tale['story'] = prepared_tale['story'].str.replace("’", "'")
    prepared_tale['story'] = prepared_tale['story'].str.replace("‘", "'")

    return prepared_tale


def apply_summarizer(summarizer, text: str) -> str:
    """Apply the summarizer to the given text."""
    result_summarizer = summarizer(text)
    return result_summarizer[0]["summary_text"]


def main(tale_path: str):
    """Execute the main process."""

    title, tale = load_tale(tale_path)
    reduced_tale = reduce_tale(tale, 5)
    prepared_tale = prepare_tale(reduced_tale)

    # 1º- Apply summarizer to each row.
    for i in tqdm(range(len(prepared_tale))):
        prepared_tale['summ'].iloc[i] = apply_summarizer(prepared_tale['story'].iloc[i])

    # Add column that indicates length.
    prepared_tale['length_story'] = prepared_tale['story'].str.len()
    prepared_tale['length_summ'] = prepared_tale['summ'].str.len()

    # 2º- Apply summarizer to previous summarizer output.
    prepared_tale['summ_2'] = ''

    for i in tqdm(range(len(prepared_tale))):
        prepared_tale['summ_2'].iloc[i] = apply_summarizer(prepared_tale['summ'].iloc[i])

    # Add length column.
    prepared_tale['length_summ_2'] = prepared_tale['summ_2'].str.len()

    # 3º- Apply summarizer to previous summarizer output.
    prepared_tale['summ_3'] = ''
    for i in tqdm(range(len(prepared_tale))):
        prepared_tale['summ_3'].iloc[i] = apply_summarizer(prepared_tale['summ_2'].iloc[i])

    # Add length column.
    prepared_tale['length_summ_3'] = prepared_tale['summ_3'].str.len()

    # Save to csv.
    prepared_tale.to_csv(f'{title}_long.csv', sep='|', encoding='utf-8')

    # Create df from df columns.
    final_tale = prepared_tale[['story', 'summ_2']]

    # Rename columns.
    final_tale.columns = ['story', 'summ']

    # Add title as first row of df.
    title = title.replace("\n", "")
    title = title.replace("-", " ")
    data = [{'story': title, 'summ': title}]
    final_tale = pd.concat([pd.DataFrame(data), final_tale], ignore_index=True)

    # Remove punctuation.
    final_tale['summ'] = final_tale['summ'].str.replace(",", "")
    final_tale['summ'] = final_tale['summ'].str.replace(";", "")
    final_tale['summ'] = final_tale['summ'].str.replace("\r", "")
    final_tale['summ'] = final_tale['summ'].str.replace("!", "")
    final_tale['summ'] = final_tale['summ'].str.replace("-", "")
    final_tale['summ'] = final_tale['summ'].str.replace("?", "")

    # Save to csv.
    final_tale.to_csv(f'{title}_short.csv', sep='|', encoding='utf-8')


if __name__ == '__main__':
    main()
