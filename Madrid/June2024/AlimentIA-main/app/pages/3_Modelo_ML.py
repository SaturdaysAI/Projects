import streamlit as st
import pandas as pd
import joblib
import os

# Título de la aplicación
st.title("AlimentIA")

# Instrucciones
st.subheader("Instrucciones:")
st.markdown("""
1. Selecciona los parámetros necesarios.
2. Pulse en CALCULAR. Depende la cantidad de artículos puede tardar unos minutos.
""")

# Cargar los modelos entrenados
@st.cache_resource
def load_models():
    models = {}
    families = ["Aceites", "Bebidas", "Bocadillos", "Bolsas", "Cc - Corte a cuchillo", "Embutidos en tercios", 
            "Hornazos", "Mq - Corte tradicional", "Merma", "Pe - Patas enteras", "Panaderia", "Quesos", 
            "Servicios", "Snacks", "Sobres al vacio", "Varios", "Vinos"]    
    for family in families:
        with open(f'models/{family}_model.joblib', 'rb') as f:
            models[family] = joblib.load(f)
    return models

models = load_models()

# Cargar las métricas
@st.cache_data
def load_metrics():
    metrics_df = pd.read_csv('metrics/cv_metrics.csv')
    return metrics_df

metrics_df = load_metrics()

# Selección de la familia de productos
family = st.selectbox("Selecciona la Familia de Productos", options=models.keys())

# Selección del período de predicción
periods = st.number_input("Número de Días a Predecir", min_value=1, value=30, step=1)

# Botón de calcular en la parte principal
if st.button("CALCULAR"):
    st.write("Calculando... Dependiendo de la cantidad de artículos, puede tardar unos minutos.")

    # Obtener el modelo seleccionado
    model = models.get(family)
    
    if model:
        future = model.make_future_dataframe(periods=periods)
        
        forecast = model.predict(future)
        
        # Formatear el DataFrame para mostrar las fechas sin horas y renombrar las columnas
        forecast['ds'] = forecast['ds'].dt.strftime('%Y-%m-%d')
        forecast = forecast.rename(columns={'ds': 'Fecha', 'yhat': 'Predicción'})
        
        # Crear columnas para dividir la página
        col1, col2 = st.columns([2, 3])
        
        with col1:
            # Mostrar los resultados
            st.write(forecast[['Fecha', 'Predicción']].tail(periods))
            
            # Mostrar las métricas
            family_metrics = metrics_df[metrics_df['Familia'] == family].drop(columns=['Familia', 'MSE'])
            st.write(family_metrics.to_html(index=False), unsafe_allow_html=True)  # Ocultar la columna de índice
        
        with col2:
            # Mostrar los gráficos
            forecast_graph_path = f'graphs/{family}_forecast.png'
            components_graph_path = f'graphs/{family}_components.png'
            
            if os.path.exists(forecast_graph_path):
                st.image(forecast_graph_path, caption='Predicción del Modelo', use_column_width=True)
            else:
                st.warning(f"Gráfico de predicción para {family} no encontrado.")
            
            if os.path.exists(components_graph_path):
                st.image(components_graph_path, caption='Componentes del Modelo', use_column_width=True)
            else:
                st.warning(f"Gráfico de componentes para {family} no encontrado.")
    else:
        st.error("Modelo no encontrado.")

# Función principal
def main():
    pass

if __name__ == "__main__":
    main()