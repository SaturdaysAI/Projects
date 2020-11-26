import re
import pandas as pd
import unidecode


def clean_word(word):
  # Remove symbols
  word = unidecode.unidecode(word)
  # Remove extra spaces
  word = word.strip()
  return word.lower()


def custom_read_csv(file):
  lines = []


  with open(file, 'r', encoding="utf8") as text:
    for line in text:
      new_line = []
      line = line.split(',"')
      for item in line:
        new_line.append(re.sub(r"[\"]+", ' ', item))
      lines.append(new_line)
  return pd.DataFrame(lines[1:],
                      columns=[clean_word(x) for x in lines[0]]+['extra'])


if __name__ == '__main__':
  file = '../../data/raw/Base de datos - Latam coronavirus.csv'
  df = custom_read_csv(file)
  df.to_csv('../../data/raw/chequeado_articles.csv', index=False)

