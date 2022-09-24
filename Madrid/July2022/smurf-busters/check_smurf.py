from rank_tracking import get_info_from_match
from util import get_data_from_account, assign_pk_to_df, get_data_from_account_max_100
import pandas as pd
from datetime import datetime
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from config import LIST_FIELDS

def get_last_10_games_account(account):
    print(f'INIT - Obteniendo datos de: {account}')
    df = get_data_from_account(account)
    print(f'datos obtenidos')
    df_with_pk = assign_pk_to_df(df)
    print(f'obtener datos scraping')
    df_rank = get_info_from_match(account)
    df_merged = pd.merge(df_with_pk, df_rank, left_on='id_match', right_on='pk_partida', how='left')
    df_merged = df_merged.loc[df_merged.summonerName == account]
    df_merged = df_merged.loc[df_merged.pk_partida.notnull()]
    print(f'END - Obteniendo datos de: {account}')
    return df_merged

def get_calculated_fields(df_account):
    df_full = df_account

    df_full['dt_fecha'] = df_full.apply(lambda x: datetime.fromtimestamp(x.ts_fecha / 1000).strftime('%d-%m-%y'),
                                        axis=1)
    df2 = df_full[['dt_fecha', 'jugador', 'pk_partida']]
    df3 = df_full[['jugador', 'pk_partida', 'individualPosition']]

    df_groupby = df3.groupby(['jugador', 'individualPosition']).size().reset_index(name='partidas_por_posicion')
    df_groupby['percentage'] = df_groupby['partidas_por_posicion'] / df_groupby.groupby('jugador')[
        'partidas_por_posicion'].transform('sum') * 100
    df_percentage_lane = df_groupby.groupby(['jugador'])['percentage'].agg('max').reset_index(name='max_recurrent_position_percentage')

    df_groupby2 = df2.groupby(['jugador', 'dt_fecha']).size().reset_index(name='mean_partidas_diarias')
    df_mean_games_per_day = df_groupby2.groupby(['jugador'], as_index=False).mean()

    df_merged_1 = pd.merge(df_full, df_percentage_lane, left_on=['jugador'], right_on=['jugador'], how='inner')
    df_merged_2 = pd.merge(df_merged_1, df_mean_games_per_day, left_on=['jugador'], right_on=['jugador'], how='inner')

    df = pd.read_csv(r"extracts/full_prepared.tsv", sep='\t')
    cols_to_del = list(set(df_merged_2.columns).difference(set(df.columns)))
    df_merged_2.drop(columns=cols_to_del, inplace=True)

    cols_to_add = list(set(df.columns).difference(set(df_merged_2.columns)))

    for col in cols_to_add:
        if col == 'smurf':
            continue
        df_merged_2[col] = 0

    df_merged_2['lps'] = df_merged_2.apply(lambda x: lp_treatment(x.lps), axis=1)
    df_merged_2.fillna(0, inplace=True)

    df_merged_2 = pd.get_dummies(df_merged_2)

    return df_merged_2


def get_model_trained():
    df = pd.read_csv(r"C:\Users\Carlos\OneDrive\Escritorio\ML\ml-lol\extracts\full_prepared2.tsv", sep='\t')
    X = df.loc[:, df.columns != 'smurf']
    Y = df['smurf']
    seed = 7
    X = pd.get_dummies(X)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, random_state=seed)

    # fit model no training data
    model = XGBClassifier()
    model.fit(X_train, y_train)

    # y_pred = model.predict(X_test)
    # predictions = [round(value) for value in y_pred]
    # # evaluate predictions
    # accuracy = accuracy_score(y_test, predictions)
    # print("Accuracy: %.2f%%" % (accuracy * 100.0))
    # print(classification_report(y_test, y_pred))
    return model


def lp_treatment(row_lp):
  if 'LP' not in str(row_lp):
    return 0
  else:
    return int(row_lp.replace('LP', ''))

if __name__ == '__main__':
    # 'Niceyneckian'
    account = 'gg fructis'
    df_account = get_last_10_games_account(account)
    df_calculated = get_calculated_fields(df_account)

    model = get_model_trained()
    predictions = model.predict(df_calculated)
    total_score = 0
    for pred in predictions:
        total_score += pred
    print(f'Probabilidad de ser smurf para el usuario {account}: {100*total_score/len(predictions)} (basado en {len(predictions)} partidas)')
