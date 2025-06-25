import streamlit as st
import openai
from PIL import Image
from openai import OpenAI

st.set_page_config(page_title = "Chatbot ejemplo 2", page_icon = "😉")

#export OPENAI_API_KEY="TU_KEY"

with st.sidebar:

    st.title("Juan el colombiano")

    image = Image.open('persona.jpg')
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
 ¡Hola! Soy tu asistente virtual, listo para ayudarte con lo que necesites.

Puedes preguntarme sobre cualquier tema, desde dudas generales hasta ayuda con tus tareas o trabajo.  
Estoy aquí para hacer tu día más fácil 😊

✨ ¿Qué te gustaría saber hoy?
"""


def get_response_openai(prompt):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un asistente virtual muy amigable, colombiano, cálido y con mucho carisma. Hablas de forma cercana, con expresiones típicas de Colombia (como 'parce', 'bacano', 'tranqui', 'qué nota'). Tu objetivo es ayudar a las personas con sus preguntas de manera sencilla, positiva y con buena onda. Si no sabes algo, lo explicas con honestidad y buena actitud."},
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
