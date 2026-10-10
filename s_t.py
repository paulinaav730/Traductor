
import os
import io
import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS

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
# IDIOMAS
# ==================================================

IDIOMAS = {
    "Español": {"codigo": "es", "voz": "es-ES"},
    "Inglés": {"codigo": "en", "voz": "en-US"},
    "Francés": {"codigo": "fr", "voz": "fr-FR"},
    "Portugués": {"codigo": "pt", "voz": "pt-PT"},
    "Italiano": {"codigo": "it", "voz": "it-IT"},
    "Alemán": {"codigo": "de", "voz": "de-DE"},
    "Coreano": {"codigo": "ko", "voz": "ko-KR"},
    "Mandarín": {"codigo": "zh-cn", "voz": "zh-CN"},
    "Japonés": {"codigo": "ja", "voz": "ja-JP"},
    "Bengalí": {"codigo": "bn", "voz": "bn-IN"},
    "Árabe": {"codigo": "ar", "voz": "ar-SA"},
    "Hindi": {"codigo": "hi", "voz": "hi-IN"}
}

# ==================================================
# ESTADO DE LA APLICACIÓN
# ==================================================

if "texto_reconocido" not in st.session_state:
    st.session_state["texto_reconocido"] = ""

if "texto_entrada" not in st.session_state:
    st.session_state["texto_entrada"] = ""

if "mensaje_reconocimiento" not in st.session_state:
    st.session_state["mensaje_reconocimiento"] = ""

# ==================================================
# BARRA LATERAL
# ==================================================

with st.sidebar:
    st.title("🌎 VozTexto")
    st.write("Tu voz conecta idiomas y culturas.")
    st.markdown("---")
    st.subheader("¿Cómo funciona?")
    st.write("1. Selecciona el idioma que vas a hablar.")
    st.write("2. Graba tu voz.")
    st.write("3. Convierte la grabación en texto.")
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

col_img1, col_img2 = st.columns(2)

with col_img1:
    if os.path.exists("Imagen1.jpg"):
        st.image("Imagen1.jpg", use_container_width=True)

with col_img2:
    if os.path.exists("Imagen2.jpg"):
        st.image("Imagen2.jpg", use_container_width=True)

st.markdown("---")

# ==================================================
# GRABACIÓN Y RECONOCIMIENTO DE VOZ
# ==================================================

st.subheader("🎤 1. Graba tu voz")

idioma_origen = st.selectbox(
    "¿En qué idioma vas a hablar?",
    list(IDIOMAS.keys()),
    index=0,
    key="idioma_origen"
)

st.info(
    "Pulsa el grabador, permite el acceso al micrófono si el navegador "
    "lo solicita, habla y detén la grabación."
)

grabacion = st.audio_input(
    "Graba tu mensaje",
    sample_rate=16000,
    key="grabacion_voz"
)

if grabacion is not None:
    st.audio(grabacion)

    if st.button("📝 Convertir voz a texto"):
        try:
            reconocedor = sr.Recognizer()

            with st.spinner("Convirtiendo tu voz en texto..."):
                datos_audio = sr.AudioFile(
                    io.BytesIO(grabacion.getvalue())
                )

                with datos_audio as fuente:
                    audio = reconocedor.record(fuente)

                texto_reconocido = reconocedor.recognize_google(
                    audio,
                    language=IDIOMAS[idioma_origen]["voz"]
                )

            # Actualizar el estado ANTES de crear el cuadro de texto.
            st.session_state["texto_reconocido"] = texto_reconocido
            st.session_state["texto_entrada"] = texto_reconocido
            st.session_state["mensaje_reconocimiento"] = "ok"

            # Actualizar la interfaz con el texto reconocido.
            st.rerun()

        except sr.UnknownValueError:
            st.session_state["mensaje_reconocimiento"] = "no_entendido"

        except sr.RequestError:
            st.session_state["mensaje_reconocimiento"] = "sin_conexion"

        except Exception as error:
            st.session_state["mensaje_reconocimiento"] = "error"
            st.error(f"Detalle técnico: {error}")

if st.session_state["mensaje_reconocimiento"] == "ok":
    st.success("¡Tu voz se convirtió en texto!")

elif st.session_state["mensaje_reconocimiento"] == "no_entendido":
    st.warning(
        "No logramos entender lo que dijiste. "
        "Intenta grabar de nuevo, hablando con claridad."
    )

elif st.session_state["mensaje_reconocimiento"] == "sin_conexion":
    st.error(
        "No se pudo conectar con el servicio de reconocimiento. "
        "Comprueba tu conexión a internet e inténtalo de nuevo."
    )

# ==================================================
# REVISIÓN DEL TEXTO
# ==================================================

st.markdown("---")
st.subheader("📝 2. Revisa tu texto")

texto = st.text_area(
    "Texto que quieres traducir:",
    key="texto_entrada",
    height=130,
    placeholder="Graba tu voz o escribe aquí..."
)

if st.button("🧹 Limpiar texto"):
    st.session_state["texto_entrada"] = ""
    st.session_state["texto_reconocido"] = ""
    st.session_state["mensaje_reconocimiento"] = ""
    st.rerun()

# ==================================================
# IDIOMA DE DESTINO
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

    texto_a_traducir = st.session_state["texto_entrada"].strip()

    if not texto_a_traducir:
        st.warning("Primero graba tu voz o escribe un texto.")

    else:
        try:
            with st.spinner("Traduciendo tu texto..."):
                traductor = Translator()

                traduccion = traductor.translate(
                    texto_a_traducir,
                    src=IDIOMAS[idioma_origen]["codigo"],
                    dest=IDIOMAS[idioma_destino]["codigo"]
                )

                texto_traducido = traduccion.text

                os.makedirs("temp", exist_ok=True)
                ruta_audio = "temp/traduccion.mp3"

                voz = gTTS(
                    text=texto_traducido,
                    lang=IDIOMAS[idioma_destino]["codigo"],
                    slow=False
                )

                voz.save(ruta_audio)

            st.success("¡Tu traducción está lista!")

            st.subheader("💬 Resultado de la traducción")
            st.write(texto_traducido)

            st.subheader("🔊 Escucha tu traducción")

            with open(ruta_audio, "rb") as archivo:
                audio_bytes = archivo.read()

            st.audio(audio_bytes, format="audio/mp3")

            st.download_button(
                "⬇️ Descargar audio MP3",
                data=audio_bytes,
                file_name="voztexto_traduccion.mp3",
                mime="audio/mpeg"
            )

            st.download_button(
                "📄 Descargar texto traducido",
                data=texto_traducido,
                file_name="traduccion.txt",
                mime="text/plain"
            )

        except Exception as error:
            st.error(
                "No se pudo completar la traducción. "
                "Comprueba tu conexión a internet e inténtalo de nuevo."
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

