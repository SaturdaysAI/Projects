import streamlit as st
import pandas as pd
import components.authenticate as authenticate
from langchain_aws import ChatBedrock
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title = 'INMILIARIA',
    layout = 'wide',
    page_icon = 'data/ai-assistant.png'
)



## PARA LA IMAGEN DE FONDO        
st.markdown("""
    <style>
    .stApp {
        background-image: url("http://gseii.org/site/wp-content/uploads/2014/05/wallpaper-628119.jpg");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

chat_container = st.container()

@st.cache_data
def get_data():

    PATH_PROCESSED = './data/processed/'
    data = pd.read_excel(PATH_PROCESSED + 'inmoDataProcessed.xlsx')

    return data


@st.cache_resource
def get_llm_model():
    
    model = ChatBedrock(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",        
        model_kwargs=dict(temperature=0),
        aws_access_key_id=st.secrets['aws_access_key_id'],
        aws_secret_access_key=st.secrets['aws_secret_access_key'],
        region_name='us-east-1',
        beta_use_converse_api=True
    )
    
    return model

# Check authentication
authenticate.set_st_state_vars()

# Add login/logout buttons
if st.session_state["authenticated"]:
    authenticate.button_logout()
else:
    authenticate.button_login()
    
if (st.session_state["authenticated"]):

    
    st.title("Chatea conmigo") 
    with chat_container:
        
        model = get_llm_model()
        data = get_data()
        
        agent = create_pandas_dataframe_agent(
            llm=model,
            df=data,
            verbose=False,
            allow_dangerous_code=True,
            agent_executor_kwargs={'handle_parsing_errors': True}
        )

        
        
        
        messages = st.container(height=400)
        if prompt := st.chat_input("Interactua"):
            
            messages.chat_message("user").write(prompt)
            
            
            respuesta = agent.invoke(prompt)
            messages.chat_message("assistant").write(f"{respuesta.get('output')}")
else:
    if st.session_state["authenticated"]:
        st.write("Usted no tene Acceso. Por favor, contáctece con el Administrador.")
    else:
        st.write("Por favor, realizar el login!")

powered_by = """ <div style="position: fixed; 
                bottom: 0; 
                right: 0; 
                width: 100%; 
                background-color: #f8f9fa; 
                text-align: right; 
                padding: 10px 20px; 
                font-size: 12px; 
                color: #6c757d;"> 
                Powered by <a href="https://sites.google.com/view/epsilon-data/" 
                target="_blank">[Epsilon Data]</a> 
                </div> """ 

# Agregar el HTML a la aplicación 
st.markdown(powered_by, unsafe_allow_html=True)

for _ in range(18):
    st.sidebar.write("")


logo_html = f"""
<div style="display: flex; align-items: center;">
    <a href="https://sites.google.com/view/epsilon-data/">
    <img src="app/static/icono_nombre.png" alt="logo" width=300 height=215>
    </a>
    <span style="font-size: 8px; font-weight: bold; color:black;"></span>
</div>
"""
st.sidebar.markdown(logo_html,unsafe_allow_html=True)
