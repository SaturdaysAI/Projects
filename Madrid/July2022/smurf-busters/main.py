from rank_tracking import get_info_from_match
from util import get_data_from_account, assign_pk_to_df
import pandas as pd



if __name__ == '__main__':
    accounts_high_elo = ["gg fructis", "ChicoRebelde","TheBoySavior 69","no tiene sendito","LambOrnnGinyin","KOI ÄITANA","Pyke Wazowskii", "KeyboardWRLD999", "Adryos Lepido","2023 Tercera","Amadeu Carvalho", "elmi uwu69", "PEŁUK1NG", "egirls above all", "ELMILLOR IS BACK", "IamDiamond", "Remember me mom", "abby me arruinó", "EL GRÁFICAS", "Laccek", "Aesenardo", "IreliaCosplayer", "Berri Vuelve Xfa", "KOI TheGrefg", "Barriga Humana", "heyy olviyonna", "Goku que", "Cabeza de Huevo", "MOTONAMl", "Ladguillos69", "Monje Shacolínn", "DuaLLipa", "CaiQi fangirl", "Weakside Jayce", "Beep bop SIUUUUU", "DevuelvanEl0ro", "TetelOl EnjoyeR"]
    # accounts_low_elo = ["HandSoIo", "IRELIAING69", "SoloQlona", "l Iove FUMAR", "ahri sIave", "abby una cosa", "XAM PING", "Amouranth Sister", "FRA KCasadο", "KatthyVipi", "Tetones", "TOAD AZULGRANA", "FTR ATTACK", " LittleRagerMilf", "EviIpain", "ahrivedercı", "Chica qué dices", "XaviSaltayAbraza", "YoGaneAMoscow5", "FUNADO PERO RICO"]
    accounts_low_elo = ["l Iove FUMAR", "ahri sIave", "abby una cosa", "XAM PING", "Amouranth Sister", "FRA KCasadο", "KatthyVipi", "Tetones", "TOAD AZULGRANA", "FTR ATTACK", " LittleRagerMilf", "EviIpain", "ahrivedercı", "Chica qué dices", "XaviSaltayAbraza", "YoGaneAMoscow5", "FUNADO PERO RICO"]
    df_final = pd.DataFrame()
    for account in accounts_low_elo:
        print(f'INIT - Obteniendo datos de: {account}')
        df = get_data_from_account(account)
        df_with_pk = assign_pk_to_df(df)
        df_rank = get_info_from_match(account)
        df_merged = pd.merge(df_with_pk, df_rank, left_on='id_match', right_on='pk_partida', how='left')
        df_merged = df_merged.loc[df_merged.summonerName == account]
        df_merged = df_merged.loc[df_merged.pk_partida.notnull()]
        df_final = pd.concat([df_final, df_merged])
        df_final.to_csv(r"C:\Users\Carlos\OneDrive\Escritorio\ML\ml-lol\extracts\full.tsv", sep='\t')  # TODO: Cambiar por ruta genérica
        print(f'END - Obteniendo datos de: {account}')
    print(f"Total de datos conseguidos de {len(accounts_low_elo)} cuentas: \n - {df_final.shape[0]} participantes \n - {int(df_final.shape[0]/10)} partidas \n - {df_final.shape[1]} columnas ")


def assign_pk_to_df(df):
    dic_match = {}
    for name, group in df.group_by('id_match'):
        list_names = []
        for match in group.iterrows():
            list_names.append(match.summonerName)
        list_names.sort()
        pk_names = '_'.join(list_names)
        dic_match[name] = pk_names
    df = df.replace(dic_match)
    return df

def df_join_match(df_match, df_rank):
    pass