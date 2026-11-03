import io

import streamlit as st
from deep_translator import GoogleTranslator, MyMemoryTranslator
from gtts import gTTS

# ---------- Page setup ----------
st.set_page_config(
    page_title="Language Translator",
    page_icon="🌐",
    layout="wide",
)

# ---------- Custom styling ----------
st.markdown(
    """
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {max-width: 1100px; padding-top: 3.5rem; padding-bottom: 2rem;}

    .app-title {
        text-align: center;
        font-size: 2.6rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 0.3rem;
        background: linear-gradient(90deg, #4f8cff, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .app-subtitle {
        text-align: center;
        opacity: 0.65;
        margin-bottom: 2rem;
        font-size: 1.05rem;
    }
    .section-label {
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        opacity: 0.6;
        margin-bottom: 0.4rem;
    }

    /* Dropdowns and text areas */
    div[data-baseweb="select"] > div {border-radius: 12px; min-height: 48px;}
    textarea {
        border-radius: 14px !important;
        font-size: 1.1rem !important;
        line-height: 1.6 !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        min-height: 46px;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #4f8cff, #8b5cf6);
        border: none;
        color: white;
        font-size: 1.05rem;
        min-height: 52px;
    }
    .stButton > button[kind="primary"]:hover {opacity: 0.9;}

    /* Output box (st.code gives us a built-in copy icon) */
    div[data-testid="stCode"] {border-radius: 14px; overflow: hidden;}
    div[data-testid="stCode"] pre {
        min-height: 205px;
        max-height: 205px;
        overflow-y: auto;
        padding: 1rem 1.1rem !important;
    }
    div[data-testid="stCode"] code {
        font-family: inherit !important;
        font-size: 1.1rem !important;
        line-height: 1.7 !important;
        white-space: pre-wrap !important;
        unicode-bidi: plaintext;
    }
    .empty-output {
        min-height: 205px;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        background: rgba(128, 128, 128, 0.12);
        opacity: 0.65;
        font-size: 1.1rem;
    }
    .service-note {font-size: 0.78rem; opacity: 0.5; margin-top: 0.4rem;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Languages list ----------
@st.cache_data
def get_languages():
    # Returns a dict like {"english": "en", "urdu": "ur", ...}
    return GoogleTranslator(source="auto", target="en").get_supported_languages(as_dict=True)


languages = get_languages()
names = sorted(languages.keys())
AUTO = "auto detect"


def pretty(name):
    return "Auto Detect" if name == AUTO else name.title()


# ---------- Default values ----------
if "src" not in st.session_state:
    st.session_state.src = AUTO
if "tgt" not in st.session_state:
    st.session_state.tgt = "urdu" if "urdu" in names else names[0]
if "input_text" not in st.session_state:
    st.session_state.input_text = ""


# ---------- Button actions ----------
def swap_languages():
    if st.session_state.src != AUTO:
        st.session_state.src, st.session_state.tgt = st.session_state.tgt, st.session_state.src
        if "result" in st.session_state:
            st.session_state.input_text = st.session_state.result
            del st.session_state["result"]


def clear_all():
    st.session_state.input_text = ""
    for key in ("result", "used"):
        st.session_state.pop(key, None)


def translate_text(text, source_name, target_name):
    """Try Google first. If it fails, use MyMemory as a backup."""
    source_code = "auto" if source_name == AUTO else languages[source_name]
    target_code = languages[target_name]
    try:
        result = GoogleTranslator(source=source_code, target=target_code).translate(text)
        return result, "Google Translate"
    except Exception:
        src = "english" if source_name == AUTO else source_name
        result = MyMemoryTranslator(source=src, target=target_name).translate(text)
        return result, "MyMemory"


# ---------- Header ----------
st.markdown('<div class="app-title">Language Translator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Translate text between more than 100 languages instantly</div>',
    unsafe_allow_html=True,
)

# ---------- Two panels: input (left) and output (right) ----------
left, right = st.columns(2, gap="large")

with left:
    st.markdown('<div class="section-label">From</div>', unsafe_allow_html=True)
    sub_a, sub_b = st.columns([5, 1], vertical_alignment="center")
    with sub_a:
        st.selectbox("From", [AUTO] + names, key="src", format_func=pretty, label_visibility="collapsed")
    with sub_b:
        st.button(
            "⇄",
            on_click=swap_languages,
            disabled=st.session_state.src == AUTO,
            help="Swap languages",
            width="stretch",
        )
    text = st.text_area(
        "Text",
        key="input_text",
        height=215,
        max_chars=4500,
        placeholder="Enter text here...",
        label_visibility="collapsed",
    )
    c1, c2 = st.columns([3, 1], vertical_alignment="center")
    with c1:
        st.caption(f"{len(text)} / 4500 characters")
    with c2:
        st.button("Clear", on_click=clear_all, width="stretch")

with right:
    st.markdown('<div class="section-label">To</div>', unsafe_allow_html=True)
    st.selectbox("To", names, key="tgt", format_func=pretty, label_visibility="collapsed")
    output_area = st.container()

# ---------- Translate button ----------
st.write("")
_, mid, _ = st.columns([1, 2, 1])
with mid:
    translate_clicked = st.button("Translate", type="primary", width="stretch")

if translate_clicked:
    if not text.strip():
        st.warning("Please enter some text to translate.")
    else:
        try:
            with st.spinner("Translating..."):
                result, used = translate_text(text, st.session_state.src, st.session_state.tgt)
            st.session_state["result"] = result
            st.session_state["target_code"] = languages[st.session_state.tgt]
            st.session_state["used"] = used
        except Exception as error:
            st.error(
                "Translation failed. Please check your internet connection "
                f"or try again in a moment. ({error})"
            )

# ---------- Output (drawn in the right panel) ----------
with output_area:
    if "result" in st.session_state:
        # The small icon at the top right of this box copies the text
        st.code(st.session_state["result"], language=None, wrap_lines=True)
        listen = st.button("🔊 Listen")
        if listen:
            try:
                tts = gTTS(text=st.session_state["result"], lang=st.session_state["target_code"])
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                st.audio(audio_buffer.getvalue(), format="audio/mp3")
            except Exception:
                st.info("Audio is not available for this language.")
        st.markdown(
            f'<div class="service-note">Translated using {st.session_state.get("used", "")}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="empty-output">Your translation will appear here...</div>',
            unsafe_allow_html=True,
        )
