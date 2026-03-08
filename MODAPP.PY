import streamlit as st
import random
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Trivia Master IUT", page_icon="💰")

# --- 1. BASE DE DATOS DE TDA (Pool de 10 preguntas) ---
if 'pool_preguntas' not in st.session_state:
    st.session_state.pool_preguntas = [
        {"p": "¿Qué norma de TV Digital se utiliza en la mayoría de Latinoamérica (incluyendo Venezuela)?", 
         "o": ["ATSC", "DVB-T", "ISDB-Tb", "DTMB"], "c": "ISDB-Tb"},
         
        {"p": "¿Qué significa la sigla TDA?", 
         "o": ["Televisión Digital Abierta", "Transmisión de Datos Automática", "Telecomunicaciones de Audio", "Terminal Digital Avanzado"], "c": "Televisión Digital Abierta"},
         
        {"p": "¿Cuál es la función principal de un Set-Top Box (Decodificador)?", 
         "o": ["Aumentar la señal WiFi", "Convertir señal digital a analógica", "Grabar programas en la nube", "Mejorar el color de la TV"], "c": "Convertir señal digital a analógica"},
         
        {"p": "¿Qué banda de frecuencia utiliza principalmente la TDA para su transmisión?", 
         "o": ["VHF", "UHF", "Microondas", "Onda Corta"], "c": "UHF"},
         
        {"p": "¿Cuál es el formato de compresión de video estándar en ISDB-Tb?", 
         "o": ["MPEG-2", "H.264 / MPEG-4 AVC", "WMV", "AVI"], "c": "H.264 / MPEG-4 AVC"},
         
        {"p": "¿Cómo se llama la señal que permite transmitir varios canales en un mismo ancho de banda?", 
         "o": ["Multiplexación", "Modulación", "Streaming", "Interferencia"], "c": "Multiplexación"},
         
        {"p": "¿Qué ventaja principal ofrece la TDA frente a la TV Analógica?", 
         "o": ["Menos canales", "Imagen con 'fantasmas'", "Alta Definición (HD) y sin ruidos", "Requiere suscripción mensual"], "c": "Alta Definición (HD) y sin ruidos"},
         
        {"p": "¿Qué componente es indispensable para recibir la señal TDA en un hogar?", 
         "o": ["Router", "Antena UHF", "Parábola de Satélite", "Cable de Fibra"], "c": "Antena UHF"},
         
        {"p": "¿Qué es el 'Ginga' en el contexto de la TDA?", 
         "o": ["Un tipo de cable", "Un middleware para interactividad", "Una marca de televisores", "El nombre de un satélite"], "c": "Un middleware para interactividad"},
         
        {"p": "¿Cuál es el ancho de banda de un canal físico en el estándar ISDB-Tb?", 
         "o": ["10 MHz", "2 MHz", "6 MHz", "12 MHz"], "c": "6 MHz"}
    ]
    # Mezclamos para que el orden cambie en cada ejecución
    random.shuffle(st.session_state.pool_preguntas)
# --- 2. GESTIÓN DEL ESTADO DEL JUEGO ---
# Usamos session_state para que la App "recuerde" en qué pregunta vamos
if 'indice' not in st.session_state:
    st.session_state.indice = 0
    st.session_state.puntos = 0
    st.session_state.juego_terminado = False

# --- 3. FUNCIONES DE AUDIO ---
# Nota para el alumno: Streamlit puede reproducir audio desde una URL
def reproducir_sonido(url):
    st.markdown(f'<audio src="{url}" autoplay style="display:none"></audio>', unsafe_allow_html=True)

# --- 4. INTERFAZ VISUAL ---
st.title("💰 ¿Quién quiere ser Ingeniero TDA?")
st.divider()

if not st.session_state.juego_terminado:
    # Obtenemos la pregunta actual del pool
    pregunta_actual = st.session_state.pool_preguntas[st.session_state.indice]
    
    st.subheader(f"Pregunta {st.session_state.indice + 1}:")
    st.write(f"### {pregunta_actual['p']}")
    
    # Creamos los botones para las opciones
    # El alumno puede cambiar el diseño de estos botones
    opciones = pregunta_actual['o']
    
    # Usamos columnas para que parezca el tablero del programa de TV
    col1, col2 = st.columns(2)
    
    with col1:
        btn_a = st.button(f"A) {opciones[0]}", use_container_width=True)
        btn_b = st.button(f"B) {opciones[1]}", use_container_width=True)
    with col2:
        btn_c = st.button(f"C) {opciones[2]}", use_container_width=True)
        btn_d = st.button(f"D) {opciones[3]}", use_container_width=True)

    # Lógica de respuesta
    seleccion = None
    if btn_a: seleccion = opciones[0]
    if btn_b: seleccion = opciones[1]
    if btn_c: seleccion = opciones[2]
    if btn_d: seleccion = opciones[3]

    if seleccion:
        if seleccion == pregunta_actual['c']:
            st.success("¡CORRECTO! 🌟")
            # AQUÍ PODRÍAS PONER UN SONIDO DE VICTORIA
            # reproducir_sonido("URL_DE_SONIDO_CORRECTO")
            st.session_state.puntos += 2
            time.sleep(1) # Pausa dramática
        else:
            st.error(f"INCORRECTO. La respuesta era: {pregunta_actual['c']} ❌")
            # reproducir_sonido("URL_DE_SONIDO_ERROR")
            time.sleep(1)

        # Avanzamos a la siguiente pregunta
        if st.session_state.indice < 4: # Solo jugamos 5 preguntas por ronda
            st.session_state.indice += 1
            st.rerun()
        else:
            st.session_state.juego_terminado = True
            st.rerun()

else:
    # PANTALLA FINAL
    st.header("🏁 ¡Fin del Juego!")
    st.metric("PUNTUACIÓN FINAL", f"{st.session_state.puntos} / 10")
    
    if st.session_state.puntos >= 8:
        st.balloons()
        st.success("¡Eres un experto! Ya puedes trabajar en la cabecera de la TDA.")
    else:
        st.warning("Sigue estudiando, la norma ISDB-Tb te espera.")
    
    if st.button("Reintentar"):
        # Limpiamos todo para empezar de nuevo
        st.session_state.indice = 0
        st.session_state.puntos = 0
        st.session_state.juego_terminado = False
        random.shuffle(st.session_state.pool_preguntas)
        st.rerun()
