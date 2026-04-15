import streamlit as st
import requests
import time
import os
from datetime import datetime

# ==========================================
# CONFIGURATION KLAYZ (SÉCURISÉE)
# ==========================================
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

# ✅ Token sécurisé via Secrets
HF_TOKEN = os.getenv("HF_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

SYSTEM_PROMPT = (
    "Tu es Klayz, une intelligence artificielle ultra-avancée, élégante et serviable. "
    "Tu réponds avec précision. Tu ne mentionnes jamais OpenAI ou Anthropic. "
    "Tu es fier d'être Klayz."
)

# ==========================================
# INTERFACE
# ==========================================
st.set_page_config(page_title="Klayz AI Interface", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top right, #1a1c23, #0e1117);
        color: #e0e0e0;
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #0b0d11 !important;
    }
    .main-title {
        background: -webkit-linear-gradient(#60efff, #00ff87);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# LOGIQUE IA
# ==========================================
def ask_klayz(messages):
    formatted_prompt = f"System: {SYSTEM_PROMPT}\n"
    
    for msg in messages:
        role = "User" if msg["role"] == "user" else "Klayz"
        formatted_prompt += f"{role}: {msg['content']}\n"
    
    formatted_prompt += "Klayz:"

    payload = {
        "inputs": formatted_prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=20)

        # Gestion des erreurs API HF
        if response.status_code == 503:
            return "⏳ Le modèle est en cours de chargement... réessaie dans quelques secondes."

        response.raise_for_status()
        res_json = response.json()

        if isinstance(res_json, list):
            return res_json[0]['generated_text'].strip()

        return "⚠️ Réponse inattendue du serveur."

    except Exception as e:
        return f"⚠️ Erreur : {str(e)}"

# ==========================================
# MÉMOIRE
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Klayz initialisé. Que veux-tu explorer ?"
    })

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("<h1 style='color: #00ff87;'>Klayz Core</h1>", unsafe_allow_html=True)
    st.write(f"📅 {datetime.now().strftime('%d/%m/%Y')}")
    
    st.divider()
    st.metric("Messages", len(st.session_state.messages))

    if st.button("🔥 Reset mémoire"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.info("Modèle : Mistral-7B")

# ==========================================
# UI CHAT
# ==========================================
st.markdown("<h1 class='main-title'>KLAYZ AI</h1>", unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# INPUT
# ==========================================
if user_input := st.chat_input("Parle à Klayz..."):
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Klayz réfléchit..."):
            answer = ask_klayz(st.session_state.messages)

            msg_placeholder = st.empty()
            full_text = ""

            for char in answer:
                full_text += char
                msg_placeholder.markdown(full_text + "▌")
                time.sleep(0.003)

            msg_placeholder.markdown(full_text)

    st.session_state.messages.append({"role": "assistant", "content": answer})
