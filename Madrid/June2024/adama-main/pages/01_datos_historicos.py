import streamlit as st
import pandas as pd
import seaborn as sns
import os



vars_dict = {"Velocidad del viento": "vel_viento",
             "Dirección del viento": "dir_viento",
             "Temperatura": "temperatura",
             "Humedad relativa": "humedad_relativa",
             "Presión barométrica": "presion_barometrica",
             "Precipitación": "precipitacion",
             "CO": "CO",
             "NO": "NO",
             "NO2": "NO2",
             "PM2.5": "PPM2_5",
             "PM10": "PPM10",
             "NOx": "NOX",
             "O3": "O3",
             "Intensidad": "intensidad",
             "Ocupación": "ocupacion",
             "Carga": "carga"}

months_list = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]


st.header('Datos históricos')
st.caption('Selecciona una variable, y un rango de años y meses para visualizar los datos históricos de la variable seleccionada en Plaza Elíptica, Madrid.')


# Sidebar for accepting input parameters
with st.sidebar:
    
    # variable = st.selectbox('Selecciona una variable', options=[x for x in vars_dict])
    
    variables = st.multiselect('Selecciona una o varias variables', options=[x for x in vars_dict])
    # year0, year1 = st.select_slider('Selecciona un rango de años', options=["2019", "2020", "2021", "2022", "2023"], value = ("2021", "2022"))
    year = st.select_slider('Selecciona un año', options=["2019", "2020", "2021", "2022", "2023"], value = "2022")
    month0, month1 = st.select_slider('Selecciona un rango de meses', options=months_list, value = ("Septiembre", "Octubre"))

    script_path = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join("\\".join(script_path.split("\\")[:-1]), "data/df_final.csv"))

# years = [str(x) for x in range(int(year0), int(year1) + 1)]
years = [year]
months = [months_list[x] for x in range(months_list.index(month0), months_list.index(month1) + 1)]

year_df = df[df['datetime'].str.split("-").str[0].isin(years)]

# print(months)
month_mapping = {'Enero': '01', 'Febrero': '02', 'Marzo': '03', 'Abril': '04', 'Mayo': '05', 'Junio': '06', 'Julio': '07', 'Agosto': '08', 'Septiembre': '09', 'Octubre': '10', 'Noviembre': '11', 'Diciembre': '12'}
month_numbers = [month_mapping.get(month, None) for month in months]
# print(month_numbers)
if month_numbers is not None:
    month_df = year_df[year_df['datetime'].str.split("-").str[1].isin(month_numbers)]
    print(month_df.shape)
else:
    st.error('Invalid month name')

# barchart = st.bar_chart(data=month_df, x='datetime', y=variable, width=0, height=0, use_container_width=True, color='#FFCC22')
colors = [x for x in sns.color_palette("viridis", as_cmap=False, n_colors=len(variables))]
linechart = st.line_chart(data=month_df, x='datetime', y=[vars_dict[variable] for variable in variables], width=0, height=0, use_container_width=True, color=colors)