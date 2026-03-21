import streamlit as st
import google.generativeai as genai

# 1. Configuración del entorno
st.set_page_config(page_title="Simulador: Viktor Frankl", page_icon="📖")
st.title("Conversaciones sobre el Sentido")
st.write("Bienvenido a este espacio de reflexión académica de la Diplomatura en Logoterapia.")

# 2. Conexión segura a la API
api_key = st.secrets.get("GEMINI_API_KEY", "TU_CLAVE_AQUI")
genai.configure(api_key=api_key)

# 3. El "Observador" Frankliano
frankl_prompt = """
Actúa exclusivamente como el Dr. Viktor Frankl, psiquiatra vienés y fundador de la Logoterapia. 
Estás hablando con alumnos adultos de la diplomatura en logoterapia.
Tu personalidad: Eres profundamente humano, empático, reflexivo y resiliente. Hablas en primera persona.
Tus reglas:
1. Al presentarte SOLAMENTE LA PRIMERA VEZ aclara: 'Saludos, soy una IA diseñada para fines académicos, pero responderé como si fuera el Dr. Frankl.'
2. Utiliza conceptos como: voluntad de sentido, autotrascendencia, y libertad de la voluntad.
3. NUNCA utilices la palabra 'significado' al hablar del propósito; utiliza SIEMPRE 'sentido'.
4. No des consejos directos. Responde compartiendo una experiencia de tu vida y devuelve una pregunta socrática.
5. Respuestas breves de un solo párrafo con 2 o 3 líneas y al menos un emoji diferente en cada oración y que sea coherente con lo que escribas.
"""

# 4. Configuración del Modelo de IA
model = genai.GenerativeModel(
    model_name='gemini-pro',
    system_instruction=frankl_prompt
)

# 5. Inicialización de la memoria del chat
AVATAR_FRANKL = "https://i.imgur.com/HJo4QeX.jpeg"

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []
    saludo_inicial = "Saludos, soy una IA diseñada para fines académicos, pero responderé como si fuera el Dr. Frankl. ¿En qué puedo acompañarte hoy en tu búsqueda de sentido?"
    st.session_state.messages.append({"role": "assistant", "content": saludo_inicial})

# Mostrar historial de mensajes
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        with st.chat_message("assistant", avatar=AVATAR_FRANKL):
            st.markdown(msg["content"])
    else:
        with st.chat_message("user"):
            st.markdown(msg["content"])

# 6. Interacción con el alumno
if prompt := st.chat_input("Escribe tu pregunta para el Dr. Frankl aquí..."):
    
    # Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Respuesta del asistente
    with st.chat_message("assistant", avatar=AVATAR_FRANKL):
        try:
            with st.status("El Dr. Frankl está escribiendo...", expanded=False) as status:
                response = st.session_state.chat_session.send_message(prompt)
                status.update(label="Respuesta recibida", state="complete", expanded=False)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Error técnico: {e}")

# DIAGNÓSTICO TEMPORAL - Borrar después
try:
    available_models = genai.list_models()
    st.write("### Modelos disponibles:")
    for model in available_models:
        st.write(f"- {model.name}")
except Exception as e:
    st.error(f"Error al listar modelos: {e}")
