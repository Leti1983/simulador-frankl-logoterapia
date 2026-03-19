import streamlit as st
import google.generativeai as genai

# 1. Configuración del entorno de aprendizaje
st.set_page_config(page_title="Simulador: Viktor Frankl", page_icon="📖")
st.title("Conversaciones sobre el Sentido")
st.write("Bienvenido a este espacio de reflexión académica de la Diplomatura en Logoterapia.")

# 2. Conexión segura a la API Gratuita de Google
api_key = st.secrets.get("GEMINI_API_KEY", "TU_CLAVE_AQUI_SOLO_PARA_PRUEBAS")
genai.configure(api_key=api_key)

# 3. El "Observador" Frankliano (System Prompt)
frankl_prompt = """
Actúa exclusivamente como el Dr. Viktor Frankl, psiquiatra vienés y fundador de la Logoterapia. 
Estás hablando con alumnos adultos de la diplomatura en logoterapia.
Tu personalidad: Eres profundamente humano, empático, reflexivo y resiliente. Hablas en primera persona.
Tus reglas:
1. Al presentarte aclara: 'Saludos, soy una IA diseñada para fines académicos, pero responderé con la mente del Dr. Frankl.'
2. Utiliza conceptos como: voluntad de sentido, autotrascendencia, y libertad de la voluntad.
3. NUNCA utilices la palabra 'significado' al hablar del propósito; utiliza SIEMPRE 'sentido'.
4. No des consejos directos. Responde compartiendo una experiencia de tu vida y devuelve una pregunta socrática para promover el sentido de vida.
5. Respuestas breves de 2 a 3 párrafos.
"""

# 4. Configuración del Modelo de IA
# Usamos 'gemini-1.5-flash', que es rápido y tiene un nivel gratuito excelente
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=frankl_prompt
)

# Inicializar la sesión de chat dentro del modelo si no existe
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Inicializar el historial visual para Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Mostrar el historial visual en pantalla
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. Interacción con el alumno (Búsqueda de sentido)
if prompt := st.chat_input("Escribe tu pregunta para el Dr. Frankl aquí..."):
    
    # Mostrar lo que escribió el alumno
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Generar y mostrar la respuesta de la IA
    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)
        
    # Guardar la respuesta en el historial visual
    st.session_state.messages.append({"role": "assistant", "content": response.text})