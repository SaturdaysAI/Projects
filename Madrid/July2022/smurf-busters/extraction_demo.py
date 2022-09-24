import pandas as pd
from check_smurf import get_calculated_fields, get_model_trained, get_last_10_games_account


df = pd.read_csv(r"extracts/full2.tsv", sep='\t')

df1 = df.loc[df.summonerName == 'elmi uwu69']
df4 = df1.loc[df1.smurf == 1].iloc[-19:]
df4_p = df1.loc[df1.smurf == 0].iloc[:2]

df2 = df.loc[df.summonerName == 'HandSoIo']
df3 = df2.loc[df2.smurf == 1].iloc[-19:]
df3_p = df2.loc[df2.smurf == 0].iloc[:2]

df_reven = pd.concat([df3, df3_p])
df_reven.drop(columns='smurf',inplace=True)
df_elmi = pd.concat([df4, df4_p])
df_elmi.drop(columns='smurf',inplace=True)

dic_dfs = {'HandSoIo':df_reven, 'elmi uwu69':df_elmi}

for account in ['PEŁUK1NG', 'SK Eckas', 'vladi1v9', '1keduii1', 'FakeRookie1', 'Jonah Falcon', 'El Hookeru']:
    df = get_last_10_games_account(account)
    dic_dfs[account] = df

dic_df_prepared={}
for account, df_account in dic_dfs.items():
    df_bueno = get_calculated_fields(df_account)
    dic_df_prepared[account] = df_bueno


for account, df_account in dic_df_prepared.items():
    df_account.to_csv(fr"extracts/{account}.tsv", sep='\t', index=False)

