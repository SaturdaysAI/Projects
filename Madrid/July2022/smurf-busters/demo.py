import pandas as pd

from check_smurf import get_model_trained


def demo():
    lista_jugadores = ['elmi uwu69', 'HandSoIo', 'PEŁUK1NG', 'SK Eckas', 'vladi1v9', '1keduii1', 'FakeRookie1', 'Jonah Falcon', 'El Hookeru', 'Go Ha Go Ha']

    dic_df_jugadores = {'summonerName': [], 'percentage': []}

    model = get_model_trained()

    for jugador in lista_jugadores:
        df = pd.read_csv(fr"C:\Users\Carlos\OneDrive\Escritorio\ML\ml-lol\extracts/{jugador}.tsv", sep='\t')
        predictions = model.predict(df)
        total_score = 0
        for pred in predictions:
            total_score += pred
        print(
            f'Probabilidad de ser smurf para el usuario {jugador}: {100 * total_score / len(predictions)} (basado en {len(predictions)} partidas)')
        dic_df_jugadores['summonerName'].append(jugador)
        dic_df_jugadores['percentage'].append(100 * total_score / len(predictions))

    return pd.DataFrame(dic_df_jugadores)

