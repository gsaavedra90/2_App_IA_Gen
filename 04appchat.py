import streamlit as st
import openai
from PIL import Image
from openai import OpenAI

st.set_page_config(page_title = "Chatbot ejemplo 2", page_icon = "😉")

#export OPENAI_API_KEY="TU_KEY"

with st.sidebar:

    st.title("Chatbot de Gaby")

    image = Image.open('happyface.jpge')
    st.image(image, caption = 'OpenAI')

    st.markdown(
        """
        Integrando OpenAI con Streamlit.
    """
    )

def clear_chat_history():
    st.session_state.messages = [{"role" : "assistant", "content": msg_chatbot}]

st.sidebar.button('Limpiar historial de chat', on_click = clear_chat_history)

msg_chatbot = """
        Soy un chatbot que está integrado a la API de OpenAI: 

        ### Preguntas frecuentes
        
        - ¿Quién eres?
        - ¿Cómo funcionas?
        - ¿Cuál es tu capacidad o límite de conocimientos?
        - ¿Puedes ayudarme con mi tarea/trabajo/estudio?
        - ¿Tienes emociones o conciencia?
        - Lo que desees
"""


def get_response_openai(prompt):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente virtual"},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=200,
        n=1
    )
    return response.choices[0].message.content


#Si no existe la variable messages, se crea la variable y se muestra por defecto el mensaje de bienvenida al chatbot.
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content" : msg_chatbot}]

# Muestra todos los mensajes de la conversación
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ingresa tu pregunta")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generar una nueva respuesta si el último mensaje no es de un assistant, sino un user
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Esperando respuesta, dame unos segundos."):
            
            response = get_response_openai(prompt)
            placeholder = st.empty()
            full_response = ''
            
            for item in response:
                full_response += item
                placeholder.markdown(full_response)

            placeholder.markdown(full_response)

    message = {"role" : "assistant", "content" : full_response}
    st.session_state.messages.append(message) #Agrega elemento a la caché de mensajes de chat.
