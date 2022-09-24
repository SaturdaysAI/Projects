import pandas as pd
from datetime import datetime

def get_score(row):
    score = 0
    if row.max_percentage > 90:
        score += 5
    elif row.max_percentage > 80:
        score += 4
    elif row.max_percentage > 70:
        score += 3
    elif row.max_percentage > 60:
        score += 2
    elif row.max_percentage > 50:
        score += 1

    if row.mean_partidas_diarias > 10:
        score += 5
    elif row.mean_partidas_diarias > 9:
        score += 4
    elif row.mean_partidas_diarias > 8:
        score += 3
    elif row.mean_partidas_diarias > 7:
        score += 2
    elif row.mean_partidas_diarias > 6:
        score += 1

    return score


df = pd.read_csv(r'C:\Users\Carlos\OneDrive\Escritorio\ML\ml-lol\extracts\full_high_elo.tsv', sep='\t')
df_2 = pd.read_csv(r'C:\Users\Carlos\OneDrive\Escritorio\ML\ml-lol\extracts\full_low_elo.tsv', sep='\t')

df_full = pd.concat([df, df_2], axis=0)

df_full['dt_fecha'] = df_full.apply(lambda x: datetime.fromtimestamp(x.ts_fecha/1000).strftime('%d-%m-%y'), axis=1)
df2 = df_full[['dt_fecha', 'jugador', 'pk_partida']]
df3 = df_full[['jugador', 'pk_partida', 'individualPosition']]


df_groupby = df3.groupby(['jugador', 'individualPosition']).size().reset_index(name='partidas_por_posicion')
df_groupby['percentage'] = df_groupby['partidas_por_posicion'] / df_groupby.groupby('jugador')['partidas_por_posicion'].transform('sum') * 100
df_percentage_lane = df_groupby.groupby(['jugador'])['percentage'].agg('max').reset_index(name='max_percentage')


df_groupby2 = df2.groupby(['jugador', 'dt_fecha']).size().reset_index(name='mean_partidas_diarias')
df_mean_games_per_day = df_groupby2.groupby(['jugador'], as_index=False).mean()

df_merged_1 = pd.merge(df_full, df_percentage_lane, left_on=['jugador'], right_on=['jugador'], how='inner')
df_merged_2 = pd.merge(df_merged_1, df_mean_games_per_day, left_on=['jugador'], right_on=['jugador'], how='inner')

df_merged_2['puntuacion_extra'] = df_merged_2.apply(lambda x: get_score(x), axis=1)

df_merged_2.drop(columns=['Unnamed: 0.2','Unnamed: 0.1', 'Unnamed: 0'], inplace=True)

df_merged_2.to_csv(r'C:\Users\Carlos\OneDrive\Escritorio\ML\ml-lol\extracts\full.tsv', sep='\t')
