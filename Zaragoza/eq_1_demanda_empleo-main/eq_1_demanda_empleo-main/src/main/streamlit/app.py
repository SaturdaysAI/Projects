from turtle import title
import streamlit as st
import pydeck as pdk
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from geopy.geocoders import Nominatim   
import config
import math
from datetime import datetime
import random


def draw_cloud(text, mask, max_word, max_font, random, colormap, background_color, width, height):
    """
        URL: https://www.holisticseo.digital/python-seo/word-cloud/
    """
    wc = WordCloud(width=width, # 800, 
                   height=height, # 800,
                   background_color=config.BACKGROUND_COLOR[background_color],                   
                   colormap=config.COLOR_MAP[colormap], # Color de las palabras. https://matplotlib.org/3.2.1/tutorials/colors/colormaps.html
                   max_words=max_word, 
                   mask=mask,
                   stopwords=config.STOPWORDS_ES, 
                   max_font_size=max_font, 
                   random_state=random) # Garantiza la reproducibilidad de la misma nube de palabras exacta
    # generate word cloud
    wc.generate(text)
        
    # show the figure
    plt.figure(figsize=(500,500))
    fig, axes = plt.subplots(1,2, gridspec_kw={'width_ratios': [3, 2]})  # horizontal: uno al lado del otro
    # fig, axes = plt.subplots(2) # vertical: uno debajo del otro   
   
    axes[0].imshow(wc, interpolation="bilinear")
    # create coloring from image
    # image_colors = ImageColorGenerator(image)
    # axes[0].imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")  

    axes[1].imshow(mask, cmap=plt.cm.gray, interpolation="bilinear")

    for ax in axes:
        ax.set_axis_off()
    st.pyplot(fig)

def draw_offert_by_criteria(criteria_list, count_list, criteria_type):
    # show the figure
    fig, ax = plt.subplots()
    width = 0.75 # the width of the bars 
    ind = np.arange(len(count_list))  # the x locations for the groups
    ax.barh(ind, count_list, width, color=(0.2, 0.4, 0.6, 0.6))
    ax.set_yticks(ind+width/2)
    ax.set_yticklabels(criteria_list, minor=False)
    plt.title("Ofertas por "+criteria_type)
    plt.xlabel("Número de ofertas")
    plt.ylabel(criteria_type)    
    x_ticks = np.arange(0, max(count_list), int(max(count_list)/len(count_list))+10)
    plt.xticks(x_ticks)   
    st.pyplot(fig)
  
def draw_offer_by_date(date_list, count_list, title):
    fig = plt.figure(figsize=(15, 7))    
    plt.plot(date_list, count_list, linewidth=1, linestyle='dashdot') # 'dashed', 'solid', 'dashdot', 'dotted'    
    plt.xlabel('Fechas')
    plt.ylabel("Cantidad de ofertas")    
    plt.title(title)
    plt.xticks(rotation = 60)
    y_int = np.arange(0, max(count_list), int(max(count_list)/len(count_list))+1)
    plt.yticks(y_int)
    plt.show()
    st.pyplot(fig)

def get_lon_lat_list(criteria_list):
    lat_lon_list = list()
    for criteria in criteria_list:   
        geolocator = Nominatim(user_agent="Your_Name")
        location = geolocator.geocode(criteria)
        lat_lon_list.append([location.longitude, location.latitude])
    return lat_lon_list


def main():
    root_path = '...'    
       
    data_path = root_path+'eq_1_demanda_empleo/resources/data/cleaned/df_data_unified.csv'
    data_df = pd.read_csv(data_path)

    sector_list = data_df['sector'].unique().tolist()
    sector_list = [x for x in sector_list if str(x) != 'nan']
    sector_list = sorted(sector_list, key=str.lower)
    province_list = data_df['province'].unique().tolist()
    
    icon_image = Image.open(root_path+'eq_1_demanda_empleo/src/main/streamlit/icon_offer.png')   
    st.set_page_config(page_title='Ofertas de Empleo en Aragón', 
                       page_icon=icon_image, # "🧊"
                       layout="centered", # "centered", "wide"
                       initial_sidebar_state="auto", # "expanded", "auto", "collapsed"
                       menu_items= None # {'About': "# This is a header. This is an *extremely* cool app!"}
                       )
    st.title('DASHBOARD para el estudio de las ofertas de empleo en Aragón')
    
    with st.form(key='offer_form'):
        st.title('Estudio de ofertas por criterio')   
        
        criteria_type = st.selectbox('Seleccione el criterio', ['Selecciona', 'Sector', 'Oficina', 'Provincia'], key=1)   
        show_data = st.checkbox('Mostrar datos', key=2)            

        if st.form_submit_button(label='Generar gráfica'):            
            if criteria_type != 'Selecciona':
                st.success('¡Ha seleccionado correctamente todas las opciones!')

                if criteria_type == 'Sector':                
                    criteria_count = data_df.pivot_table(columns=['sector'], aggfunc='size')
                elif criteria_type == 'Oficina':
                    criteria_count = data_df.pivot_table(columns=['office'], aggfunc='size')
                elif criteria_type == 'Provincia':
                    criteria_count = data_df.pivot_table(columns=['province'], aggfunc='size')         
                criteria_count_df = pd.DataFrame({'criteria':criteria_count.index, 'count':criteria_count.values}).reset_index(drop=True)                
                criteria_list = criteria_count_df['criteria'].tolist()
                count_list = criteria_count_df['count'].tolist()
                                
                draw_offert_by_criteria(criteria_list, count_list, criteria_type)
                if show_data:
                    st.table(criteria_count_df)                    
            else:
                st.warning('Por favor, compruebe que ha seleccionado entre las opciones disponibles.')            
    with st.form(key='temporary_form'):
        st.title('Estudio de ofertas por fecha')

        sub_data_df = data_df[['date', 'province', 'sector']]
        date_list = data_df['date'].tolist()
        
        year_list = list()
        for date in date_list:
            # year = int(date.split('/')[2])
            year = int(date.split('-')[0])
            if year not in year_list:
                year_list.append(year)
        year_list = sorted(year_list, key=int, reverse=False)

        year_selected = st.selectbox('Seleccione el año', ['Selecciona todos']+list(map(str, year_list)), key=1)
        sector_type = st.selectbox('Seleccione el sector laboral', ['Selecciona todos']+sector_list, key=2)
        #filtered_province_list = list(filter(None, province_list))
        filtered_province_list = [province for province in province_list if str(province) != 'nan']
        province_type = st.selectbox('Seleccione la provincia', ['Selecciona todos']+ filtered_province_list , key=3)        
        title = "Ofertas teniendo en cuenta: "

        if st.form_submit_button(label='Generar gráfica'):  
                         
            # YEAR
            if year_selected != 'Selecciona todos' and sector_type == 'Selecciona todos' and province_type == 'Selecciona todos':
                st.success('¡Ha seleccionado correctamente todas las opciones!')
                final_data_df = sub_data_df[sub_data_df['date'].str.contains(str(year_selected))]
                # final_data_df["date"] = pd.to_datetime(final_data_df["date"], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
                final_data_df = final_data_df.sort_values(by="date")
                title += 'AÑO'
            # SECTOR
            elif year_selected == 'Selecciona todos' and sector_type != 'Selecciona todos' and province_type == 'Selecciona todos':
                st.success('¡Ha seleccionado correctamente todas las opciones!')
                #sub_data_df["date"] = pd.to_datetime(sub_data_df["date"], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
                sub_data_df = sub_data_df.sort_values(by="date")
                final_data_df = sub_data_df.loc[sub_data_df['sector'] == sector_type, ['date']]  
                title += 'SECTOR'
            # PROVINCE
            elif year_selected == 'Selecciona todos' and sector_type == 'Selecciona todos' and province_type != 'Selecciona todos':
                st.success('¡Ha seleccionado correctamente todas las opciones!')
                #sub_data_df["date"] = pd.to_datetime(sub_data_df["date"], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
                sub_data_df = sub_data_df.sort_values(by="date")
                final_data_df = sub_data_df.loc[sub_data_df['province'] == province_type, ['date']]
                title += 'PROVINCIA'  
            # YEAR + SECTOR
            elif year_selected != 'Selecciona todos' and sector_type != 'Selecciona todos' and province_type == 'Selecciona todos':
                st.success('¡Ha seleccionado correctamente todas las opciones!')
                sector_data_df = sub_data_df.loc[sub_data_df['sector'] == sector_type, ['date']]
                # sector_data_df["date"] = pd.to_datetime(sector_data_df["date"], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
                sector_data_df = sector_data_df.sort_values(by="date")           
                final_data_df = sector_data_df[sector_data_df['date'].str.contains(str(year_selected))] 
                title += 'AÑO, SECTOR'
            # YEAR + PROVINCE
            elif year_selected != 'Selecciona todos' and sector_type == 'Selecciona todos' and province_type != 'Selecciona todos':
                st.success('¡Ha seleccionado correctamente todas las opciones!')
                province_data_df = sub_data_df.loc[sub_data_df['province'] == province_type, ['date']]
                # province_data_df["date"] = pd.to_datetime(province_data_df["date"], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
                province_data_df = province_data_df.sort_values(by="date")
                final_data_df = province_data_df[province_data_df['date'].str.contains(str(year_selected))]   
                title += 'AÑO, PROVINCIA'                           
            # SECTOR + PROVINCE
            elif year_selected == 'Selecciona todos' and sector_type != 'Selecciona todos' and province_type != 'Selecciona todos':
                st.success('¡Ha seleccionado correctamente todas las opciones!')    
                sector_data_df = sub_data_df.loc[sub_data_df['sector'] == sector_type, ['date', 'province']]
                # sector_data_df["date"] = pd.to_datetime(sector_data_df["date"], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
                sector_data_df = sector_data_df.sort_values(by="date")
                final_data_df = sector_data_df.loc[sector_data_df['province'] == province_type, ['date']]
                title += 'SECTOR, PROVINCIA'
            # YEAR + SECTOR + PROVINCE
            elif year_selected != 'Selecciona todos' and sector_type != 'Selecciona todos' and province_type != 'Selecciona todos':
                st.success('¡Ha seleccionado correctamente todas las opciones!')
                sector_data_df = sub_data_df.loc[sub_data_df['sector'] == sector_type, ['date', 'province']]
                # sector_data_df["date"] = pd.to_datetime(sector_data_df["date"], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
                sector_data_df = sector_data_df.sort_values(by="date")                    
                province_data_df = sector_data_df.loc[sector_data_df['province'] == province_type, ['date']]
                final_data_df = province_data_df[province_data_df['date'].str.contains(str(year_selected))] 
                title += 'AÑO, SECTOR, PROVINCIA' 
            else:
                # st.warning('Por favor, compruebe que ha seleccionado a menos una de las opciones disponibles.') 
                final_data_df = sub_data_df
                title += 'TODO' 
            date_count = final_data_df.pivot_table(columns=['date'], aggfunc='size')
            date_count_df = pd.DataFrame({'date':date_count.index, 'count':date_count.values}).reset_index(drop=True)                    
            draw_offer_by_date(date_list=date_count_df['date'].tolist(), count_list=date_count_df['count'].astype(int).tolist(), title=title)

    with st.form(key='word_cloud_form'):
            st.title('Nube de palabras')
            
            content_type = st.selectbox('Seleccione tipo de contenido', ['Selecciona', 'Ofertas', 'Descripción'], key=1)            
            sector_type = st.selectbox('Seleccione el sector laboral', ['Selecciona']+sector_list, key=2)
                        
            background_color = st.selectbox('Seleccione el color del fondo', ['Selecciona', 'negro', 'blanco', 'salmón'], key=3)
            colormap = st.selectbox('Seleccione el color de las palabras', ['Selecciona', 'caliente', 'arcoiris', 'sísmico', 'pastel'], key=4)

            # width = st.slider(label='Ancho', min_value=200, max_value=1000, key=5) 
            # height = st.slider(label='Altura', min_value=200, max_value=1000, key=6) 
            
            max_word = st.slider(label='Máximo de palabras', min_value=200, max_value=1000, key=7)            
            max_font = st.slider(label='Tamaño máximo del fondo', min_value=50, max_value=350, key=8)             
            
            random = st.slider(label='Estado aleatorio', min_value=30, max_value=100, key=9)            
            
            image_upload = st.file_uploader("Suba una imagen para usar su forma (preferiblemente de tipo silhouette)", key=10)             
        
            if content_type == 'Ofertas':
                column_name = 'job'
            elif content_type == 'Descripción':
                column_name = 'content'      
            if st.form_submit_button(label='Generar nube'):
                if content_type != 'Selecciona' and colormap != 'Selecciona' and sector_type!= 'Selecciona' and background_color != 'Selecciona' and image_upload:            
                    st.success('¡Ha seleccionado correctamente todas las opciones!')

                    # Filtering by sector and type of content:
                    if sector_type == 'Todas':                        
                        text = ' '.join(data_df[column_name].tolist())
                    else:
                        sub_data_df = data_df.loc[data_df['sector'] == sector_type, ['job', 'content']] # ,'requirement'   
                        filter_list = [x for x in sub_data_df[column_name].tolist() if str(x) != 'nan']            
                        text = ' '.join(filter_list)                    

                    mask = np.array(Image.open(image_upload))
                    # st.image(image, width=100, use_column_width=True)            
                    # cloud(image, column_name=column_name, max_word=max_word, max_font=max_font, random=random)
                    st.write(draw_cloud(text=text,
                                        mask=mask, 
                                        max_word=max_word, 
                                        max_font=max_font, 
                                        random=random, 
                                        colormap=colormap, 
                                        background_color=background_color, 
                                        width= 200, # width, 
                                        height=200,), # height
                                        use_column_width=True)
                else:
                    st.warning('Por favor, compruebe que ha seleccionado entre las opciones disponibles.')

    with st.form(key='geographic_form'):
        st.title('Mapa de ofertas')

        criteria_type = st.selectbox('Seleccione el criterio', ['Selecciona', 'Provincia', 'Ciudad', 'Oficina'], key=1)        

        if st.form_submit_button(label='Ubicar ofertas en mapa'):            
            if criteria_type != 'Selecciona':
                st.success('¡Ha seleccionado correctamente todas las opciones!')
                
                if criteria_type == 'Provincia':
                    criteria_count = data_df.pivot_table(columns=['province'], aggfunc='size')                                     
                elif criteria_type == 'Ciudad':
                    criteria_count = data_df.pivot_table(columns=['city'], aggfunc='size')   
                elif criteria_type == 'Oficina':
                    criteria_count = data_df.pivot_table(columns=['office'], aggfunc='size')

                criteria_count_df = pd.DataFrame({'criteria':criteria_count.index, 'count':criteria_count.values}).reset_index(drop=True)
                # Use pandas to calculate additional data
                criteria_count_df["count_radius"] = criteria_count_df["count"].apply(lambda count: count*70)
                criteria_list = criteria_count_df['criteria'].tolist()                               
                # print(criteria_list)
                criteria_count_df["location"] = get_lon_lat_list(criteria_list)   
                # print(criteria_count_df)
                # Define a layer to display on a map
                layer = pdk.Layer(
                                    "ScatterplotLayer",
                                    criteria_count_df,
                                    pickable=True,
                                    opacity=0.8,
                                    stroked=True,
                                    filled=True,
                                    radius_scale=6,
                                    radius_min_pixels=1,
                                    radius_max_pixels=100,
                                    line_width_min_pixels=1,
                                    get_position="location",
                                    get_radius="count_radius",
                                    get_fill_color=[255, 140, 0],
                                    get_line_color=[0, 0, 0],
                                )
                # Set the viewport location:
                view_state = pdk.ViewState(latitude=41.303823, longitude=-1.220740, zoom=7, bearing=0, pitch=0)

                # Render
                r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{criteria}\n{count}"})
                # r.to_html("scatterplot_layer.html")  
                st.pydeck_chart(r)                       
            else:
                st.warning('Por favor, compruebe que ha seleccionado entre las opciones disponibles.')


if __name__=="__main__":
  main()