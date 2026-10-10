
import os
import streamlit as st
from googletrans import Translator
from gtts import gTTS
from bokeh.models import Button, CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

# ==================================================
# CONFIGURACIÓN
# ==================================================

st.set_page_config(
    page_title="VozTexto | Traductor",
    page_icon="🌎",
    layout="centered"
)

# ==================================================
# ESTILOS
# ==================================================

st.markdown("""
<style>
    .stApp {
        background-color: #FFF8F0;
    }

    .block-container {
        max-width: 950px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #8C451D;
    }

    .hero {
        background: linear-gradient(135deg, #FFAD70, #F07836);
        padding: 30px 20px;
        border-radius: 22px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 5px 18px rgba(140, 69, 29, 0.12);
    }

    .hero h1 {
        color: white;
        font-size: 42px;
        margin: 0;
    }

    .hero p {
        color: white;
        font-size: 17px;
        margin: 8px 0 0 0;
    }

    .description {
        text-align: center;
        color: #76533D;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .section-card {
        background: white;
        border: 1px solid #F0D8C5;
        padding: 20px;
        border-radius: 18px;
        margin: 12px 0;
    }

    div.stButton > button {
        background: #F07836;
        color: white;
        border: none;
        border-radius: 12px;
        min-height: 46px;
        font-weight: 600;
        width: 100%;
    }

    div.stButton > button:hover {
        background: #D95D23;
        color: white;
        border: none;
    }

    [data-testid="stSidebar"] {
        background-color: #FFF0E2;
    }

    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ==================================================
# IDIOMAS DISPONIBLES
# ==================================================

IDIOMAS = {
    "Español": {
        "codigo": "es",
        "voz": "es-ES"
    },
    "Inglés": {
        "codigo": "en",
        "voz": "en-US"
    },
    "Francés": {
        "codigo": "fr",
        "voz": "fr-FR"
    },
    "Portugués": {
        "codigo": "pt",
        "voz": "pt-PT"
    },
    "Italiano": {
        "codigo": "it",
        "voz": "it-IT"
    },
    "Alemán": {
        "codigo": "de",
        "voz": "de-DE"
    },
    "Coreano": {
        "codigo": "ko",
        "voz": "ko-KR"
    },
    "Mandarín": {
        "codigo": "zh-cn",
        "voz": "zh-CN"
    },
    "Japonés": {
        "codigo": "ja",
        "voz": "ja-JP"
    },
    "Bengalí": {
        "codigo": "bn",
        "voz": "bn-IN"
    },
    "Árabe": {
        "codigo": "ar",
        "voz": "ar-SA"
    },
    "Hindi": {
        "codigo": "hi",
        "voz": "hi-IN"
    }
}

# ==================================================
# BARRA LATERAL
# ==================================================

with st.sidebar:
    st.title("🌎 VozTexto")
    st.write("Tu voz conecta idiomas y culturas.")
    st.markdown("---")
    st.subheader("¿Cómo funciona?")
    st.write("1. Selecciona el idioma que vas a hablar.")
    st.write("2. Pulsa el botón del micrófono.")
    st.write("3. Revisa el texto reconocido.")
    st.write("4. Selecciona el idioma de destino.")
    st.write("5. Traduce y escucha el resultado.")
    st.markdown("---")
    st.caption("Proyecto de procesamiento de lenguaje natural.")

# ==================================================
# ENCABEZADO E IMÁGENES
# ==================================================

st.markdown("""
<div class="hero">
    <h1>🌎 VozTexto</h1>
    <p>Habla. Traduce. Conecta.</p>
</div>

<div class="description">
    Rompe las barreras del idioma usando tu voz.
</div>
""", unsafe_allow_html=True)

# Las imágenes deben estar en la raíz del repositorio.

col_img1, col_img2 = st.columns(2)

with col_img1:
    if os.path.exists("Imagen1.jpg"):
        st.image(
            "Imagen1.jpg",
            use_container_width=True
        )
    else:
        st.info("Agrega Imagen1.jpg al repositorio.")

with col_img2:
    if os.path.exists("Imagen2.jpg"):
        st.image(
            "Imagen2.jpg",
            use_container_width=True
        )
    else:
        st.info("Agrega Imagen2.jpg al repositorio.")

st.markdown("---")

# ==================================================
# SELECCIÓN DEL IDIOMA DE ORIGEN
# ==================================================

st.subheader("🎤 1. Habla para comenzar")

idioma_origen = st.selectbox(
    "¿En qué idioma vas a hablar?",
    list(IDIOMAS.keys()),
    index=0,
    key="idioma_origen"
)

st.caption(
    "Permite el acceso al micrófono cuando tu navegador lo solicite."
)

codigo_voz = IDIOMAS[idioma_origen]["voz"]

# ==================================================
# RECONOCIMIENTO DE VOZ
# ==================================================

stt_button = Button(
    label="🎤 Escuchar mi voz",
    width=300,
    height=55
)

stt_button.js_on_event(
    "button_click",
    CustomJS(code=f"""
        const SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition;

        if (!SpeechRecognition) {{
            document.dispatchEvent(
                new CustomEvent("GET_TEXT", {{
                    detail: "ERROR_BROWSER"
                }})
            );
        }} else {{
            const recognition = new SpeechRecognition();

            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = "{codigo_voz}";

            recognition.onresult = function(event) {{
                const texto =
                    event.results[0][0].transcript;

                document.dispatchEvent(
                    new CustomEvent("GET_TEXT", {{
                        detail: texto
                    }})
                );
            }};

            recognition.onerror = function(event) {{
                document.dispatchEvent(
                    new CustomEvent("GET_TEXT", {{
                        detail: "ERROR:" + event.error
                    }})
                );
            }};

            recognition.start();
        }}
    """)
)

resultado_microfono = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="reconocimiento_voz",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

if resultado_microfono and "GET_TEXT" in resultado_microfono:
    resultado = resultado_microfono["GET_TEXT"]

    if resultado == "ERROR_BROWSER":
        st.error(
            "Tu navegador no admite reconocimiento de voz. "
            "Prueba con Google Chrome."
        )
    elif resultado.startswith("ERROR:"):
        st.error(
            "No se pudo reconocer la voz. Revisa los permisos "
            "del micrófono e inténtalo de nuevo."
        )
    else:
        st.session_state["texto_reconocido"] = resultado

# ==================================================
# TEXTO RECONOCIDO O ESCRITO
# ==================================================

st.markdown("---")
st.subheader("📝 2. Revisa tu texto")

if "texto_reconocido" not in st.session_state:
    st.session_state["texto_reconocido"] = ""

texto = st.text_area(
    "El texto que quieres traducir:",
    key="texto_entrada",
    value=st.session_state["texto_reconocido"],
    height=130,
    placeholder="Habla con el micrófono o escribe aquí..."
)

# ==================================================
# SELECCIÓN DEL IDIOMA DE DESTINO
# ==================================================

st.subheader("🌐 3. Elige el idioma de traducción")

idiomas_destino = [
    idioma for idioma in IDIOMAS
    if idioma != idioma_origen
]

idioma_destino = st.selectbox(
    "¿A qué idioma quieres traducir?",
    idiomas_destino,
    index=0,
    key="idioma_destino"
)

# ==================================================
# TRADUCCIÓN Y GENERACIÓN DE AUDIO
# ==================================================

st.markdown("---")

if st.button("✨ Traducir y generar audio"):

    if not texto.strip():
        st.warning(
            "Primero habla con el micrófono o escribe un texto."
        )

    else:
        try:
            with st.spinner("Traduciendo tu texto..."):

                traductor = Translator()

                traduccion = traductor.translate(
                    texto.strip(),
                    src=IDIOMAS[idioma_origen]["codigo"],
                    dest=IDIOMAS[idioma_destino]["codigo"]
                )

                texto_traducido = traduccion.text

                os.makedirs("temp", exist_ok=True)

                ruta_audio = "temp/traduccion.mp3"

                audio = gTTS(
                    text=texto_traducido,
                    lang=IDIOMAS[idioma_destino]["codigo"],
                    slow=False
                )

                audio.save(ruta_audio)

            st.success("¡Tu traducción está lista!")

            st.markdown(
                '<div class="section-card">'
                '<h3>💬 Resultado de la traducción</h3>'
                '</div>',
                unsafe_allow_html=True
            )

            st.write(texto_traducido)

            st.subheader("🔊 Escucha tu traducción")

            with open(ruta_audio, "rb") as archivo:
                audio_bytes = archivo.read()

            st.audio(
                audio_bytes,
                format="audio/mp3"
            )

            st.download_button(
                label="⬇️ Descargar audio MP3",
                data=audio_bytes,
                file_name="voztexto_traduccion.mp3",
                mime="audio/mpeg"
            )

            st.download_button(
                label="📄 Descargar texto traducido",
                data=texto_traducido,
                file_name="traduccion.txt",
                mime="text/plain"
            )

        except Exception as error:
            st.error(
                "No se pudo completar la traducción. "
                "Comprueba tu conexión a internet e inténtalo otra vez."
            )
            st.caption(f"Detalle técnico: {error}")

# ==================================================
# PIE DE PÁGINA
# ==================================================

st.markdown("---")

st.markdown("""
<div style="text-align:center; padding:15px; color:#8C451D;">
    <strong>VozTexto 🌎</strong>
    <p>La tecnología nos acerca, sin importar el idioma.</p>
</div>
""", unsafe_allow_html=True)
