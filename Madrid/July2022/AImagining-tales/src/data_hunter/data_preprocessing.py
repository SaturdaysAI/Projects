import logging
import os
import re

import pandas as pd
from tqdm import tqdm


logger = logging.getLogger(__name__)

# Output paths for the preprocessed datasets.
STORIES_PATH = './scraped_data/stories'
SUMMARIES_PATH = './scraped_data/summaries'
ALIGNMENTS_PATH = './scraped_data/manual_alignments'
PREPROCESSED_DATA_PATH = './preprocessed_data'


def setup_environment():
    """Set up the environment."""

    for data_path in [STORIES_PATH, SUMMARIES_PATH, ALIGNMENTS_PATH]:
        if not os.path.exists(data_path):
            raise Exception(f"The path '{data_path}' does not exist.")

    os.makedirs(PREPROCESSED_DATA_PATH, exist_ok=True)


def get_alignments_titles() -> list[str]:
    """Get the list of manual alignments."""

    align_titles = []
    for title in os.listdir(ALIGNMENTS_PATH):
        align_titles.append(title)

    logger.debug('We have {} titles with manual alignments.'.format(len(align_titles)))

    return align_titles


def get_stories_df() -> pd.DataFrame:
    """Get the stories DataFrame."""

    # Each row is a dictionary. The rows set is a list of dictionaries.
    list_rows = []

    # Iterate over stories titles.
    alignments = get_alignments_titles()

    for title in os.listdir(STORIES_PATH):
        if title in alignments:
            # Iterate over each title chapter.
            folder_title = os.path.join(STORIES_PATH, title)

            for chapter in os.listdir(folder_title):
                # Each time a new chapter starts, reset the paragraph counter.
                # The paragraph counter.
                cont_p = 0

                # The number of the chapter is taken from the filename.
                chapter_name = folder_title + '/' + chapter
                # The filename is *.txt.utf8 --> We take everything before the .txt.utf8
                c = chapter[:-9]

                # Read each chapter's file.
                with open(chapter_name, mode="r", encoding="utf-8") as file:
                    text = file.read()
                    # Each paragraph is separated by two carriage return.
                    # It would be equivalent to use the .splitlines().
                    p = text.split("\n\n")

                for i in range(len(p)):
                    row = {'title': title, 'chapter': int(c), 'paragraph': cont_p, 'text': p[i]}
                    list_rows.append(row)
                    cont_p += 1

            logger.debug(f'Finished processing the title: {title}')

    stories = pd.DataFrame(list_rows, columns=['title', 'chapter', 'paragraph', 'text'])
    stories['len_text'] = stories['text'].str.len()
    stories = stories[stories.len_text != 0]

    return stories


def get_summaries_df() -> pd.DataFrame:
    """Get the summaries DataFrame."""

    # Each row is a dictionary. The rows set is a list of dictionaries.
    list_rows = []

    # Iterate over stories titles.
    alignments = get_alignments_titles()

    for title in os.listdir(SUMMARIES_PATH):
        if title in alignments:
            # Iterate over each title chapter.
            folder_title = os.path.join(SUMMARIES_PATH, title)
            for chapter in os.listdir(folder_title):
                # Each time a new chapter starts, reset the paragraph counter.
                # The paragraph counter.
                cont_p = 0

                # The number of the chapter is taken from the filename.
                chapter_name = folder_title + '/' + chapter
                # The filename is *.txt.utf8 --> We take everything before the .txt.utf8
                c = chapter[:-9]

                # Read each chapter's file.
                with open(chapter_name, mode="r", encoding="utf-8") as file:
                    text = file.read()
                    # Each paragraph is separated by two carriage return.
                    # It would be equivalent to use the .splitlines().
                    p = text.split("\n\n")

                for i in range(len(p)):
                    row = {'title': title, 'chapter': int(c), 'paragraph': cont_p, 'text': p[i]}
                    list_rows.append(row)
                    cont_p += 1

            logger.debug(f'Finished processing the title: {title}')

    summaries = pd.DataFrame(list_rows, columns=['title', 'chapter', 'paragraph', 'text'])
    summaries['len_text'] = summaries['text'].str.len()
    summaries = summaries[summaries.len_text != 0]
    summaries = summaries.drop(columns='len_text')

    return summaries


def get_alignments_df() -> pd.DataFrame:
    """Get the alignments DataFrame."""

    # Each row is a dictionary. The rows set is a list of dictionaries.
    list_rows = []

    # Iterate over stories titles.
    for title in os.listdir(ALIGNMENTS_PATH):
        # Iterate over each title chapter.
        folder_title = os.path.join(ALIGNMENTS_PATH, title)
        for chapter in os.listdir(folder_title):
            # Each time a new chapter starts, reset the paragraph counter.
            # The paragraph counter.
            cont_p = 0

            # The number of the chapter is taken from the filename.
            chapter_name = folder_title + '/' + chapter
            # The filename is *.txt --> We take everything before the .txt
            c = chapter[:-4]

            # Read each chapter's file.
            with open(chapter_name, mode="r", encoding="utf-8") as file:
                text = file.read()
                # Each paragraph is separated by a carriage return.
                # It would be equivalent to use the .splitlines().
                p = text.split("\n")

            for i in range(len(p)):
                row = {'title': title, 'chapter': int(c), 'paragraph': cont_p, 'text': p[i]}
                list_rows.append(row)
                cont_p += 1

        logger.debug(f'Finished processing the title: {title}')

    alignments = pd.DataFrame(list_rows, columns=['title', 'chapter', 'paragraph', 'text'])
    alignments = alignments.drop(columns='paragraph')
    alignments['split1'] = alignments['text'].str.split(': ', 1).str[0]
    alignments['split2'] = alignments['text'].str.split(': ', 1).str[1]
    alignments['split1'] = alignments['split1'].str[1:]
    alignments['split2'] = alignments['split2'].str[:-1]

    return alignments


def get_dataframes() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Get the stories, summaries and alignments DataFrames."""

    stories_df = get_stories_df()
    stories_df.dropna(inplace=True)
    stories_path = os.path.join(PREPROCESSED_DATA_PATH, 'stories.csv')
    stories_df.to_csv(stories_path, index=False)

    summaries_df = get_summaries_df()
    summaries_df.dropna(inplace=True)
    summaries_path = os.path.join(PREPROCESSED_DATA_PATH, 'summaries.csv')
    summaries_df.to_csv(summaries_path, index=False)

    alignments_df = get_alignments_df()
    alignments_df.dropna(inplace=True)
    alignments_path = os.path.join(PREPROCESSED_DATA_PATH, 'alignments.csv')
    alignments_df.to_csv(alignments_path, index=False)

    return stories_df, summaries_df, alignments_df


def merge_dataframes(stories_df: pd.DataFrame, summaries_df: pd.DataFrame,
                     alignments_df: pd.DataFrame) -> pd.DataFrame:
    """Combine the stories, summaries and alignments DataFrames."""

    all_df = alignments_df.copy()

    # -----------------------
    # -- Add the summaries --
    # -----------------------

    all_df["summary_text"] = ""

    # Iterate over all DataFrame rows.
    for i in range(len(all_df)):

        # Save the title, chapter number and paragraph number for each row.
        t = all_df['title'].iloc[i]
        num_chapter = str(all_df['chapter'].iloc[i])
        num_p_summ = str(all_df['split1'].iloc[i])

        if bool(re.search('\d', num_p_summ)):
            num_p_summ = re.sub(':', '', num_p_summ)

            # Fill the new column with the correspondent summaries having into
            # account the number of chapter and the number of paragraph.
            text = summaries_df[
                (summaries_df.title == t) &
                (summaries_df.chapter == int(num_chapter)) &
                (summaries_df.paragraph == int(num_p_summ))
            ].text.values

            all_df['summary_text'].iloc[i] = '\n\n'.join(list(text))

    # ---------------------
    # -- Add the stories --
    # ---------------------

    all_df["story_text"] = ""
    all_df['split2'] = all_df['split2'].astype(str)

    # Iterate over DataFrame rows to add the story text.
    for i in tqdm(range(len(all_df))):
        # Save the title, chapter number and paragraph number for each row.
        t = all_df['title'].iloc[i]
        num_chapter = all_df['chapter'].iloc[i]
        # List to save all the paragraphs that correspond to a summary.
        l = []

        # 1 - Search each value, split by separator (comma) and iterate.
        values = all_df.iloc[i].split2

        if bool(re.search('\d', values)):
            split = values.split(',')
            for s in split:
                # num_paragraph_stories
                num_p_st = int(s.strip())
                text = stories_df[
                    (stories_df.title == t) &
                    (stories_df.chapter == num_chapter) &
                    (stories_df.paragraph == num_p_st)
                ].text.values

                l.append("\n\n".join(text))

            # 2 - Save the story text.
            all_df['story_text'].iloc[i] = "\n\n".join(l)

    return all_df


def get_merged_df():
    """Get the combined DataFrame."""

    stories_df, summaries_df, alignments_df = get_dataframes()
    data_df = merge_dataframes(stories_df, summaries_df, alignments_df)
    data_df.dropna(inplace=True)
    data_path = os.path.join(PREPROCESSED_DATA_PATH, 'data.csv')
    data_df.to_csv(data_path, index=False)


def load_dataframe(filename: str) -> pd.DataFrame:
    """Load data from a file in the preprocessed path."""

    path = os.path.join(PREPROCESSED_DATA_PATH, filename)
    dataframe = pd.read_csv(path)

    return dataframe


if __name__ == '__main__':

    # Logging format.
    LOG_FORMAT = '%(asctime)s - %(levelname)s: %(message)s'
    LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=LOG_DATEFORMAT)

    # Execute the main process.
    setup_environment()
    # df = load_dataframe('data.csv')
    get_merged_df()
