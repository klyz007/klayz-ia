import streamlit as st
import requests
import time
import json
from datetime import datetime

# ===================== CONFIGURATION =====================
st.set_page_config(
    page_title="Klayz IA - Neural Interface",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS avancé
st.markdown("""
    <style>
    .main { background-color: #0a0e17; color: #e0e0ff; }
    .stChatMessage { border-radius: 15px; padding: 15px; margin: 10px 0; }
    .user-bubble { background-color: #1e3a8a; border-radius: 18px 18px 0 18px; padding: 10px; }
    .assistant-bubble { background-color: #1f2937; border-radius: 18px 18px 18px 0; padding: 10px; }
    .header { font-size: 42px; font-weight: bold; color: #00f5ff; text-align: center; margin-bottom: 10px; }
    .subheader { font-size: 18px; color: #94a3b8; text-align: center; }
    .typing { color: #67e8f9; animation: blink 1s step-end infinite; }
    @keyframes blink { 50% { opacity: 0; } }
    </style>
""", unsafe_allow_html=True)

# ===================== TITRE & DESCRIPTION =====================
st.markdown('<p class="header">⚡ KLAYZ IA</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Neural Intelligence v2.8 • Officiel</p>', unsafe_allow_html=True)
st.divider()

# ===================== SIDEBAR =====================
with st.sidebar:
    st.header("🔧 Système Klayz")
    st.success("● En ligne")
    
    st.metric("Modèle", "Mistral-7B", "Stable")
    st.progress(92, text="Capacité neuronale : 92%")
    
    st.divider()
    if st.button("🗑️ Réinitialiser Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption("Développé par Klyz007")

# ===================== INITIALISATION =====================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Salut ! Je suis **Klayz**, ton IA personnelle. Pose-moi n'importe quelle question ! 😊"}
    ]

# ===================== AFFICHAGE DES MESSAGES =====================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ===================== FONCTION API (SÉCURISÉE) =====================
def query_klayz(prompt, history):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    
    # RÉCUPÉRATION DU TOKEN DEPUIS LES SECRETS (PAS EN CLAIR !)
    try:
        token = st.secrets["HF_TOKEN"]
    except:
        return "Erreur : Le token 'HF_TOKEN' n'est pas configuré dans les Secrets de Streamlit."

    headers = {"Authorization": f"Bearer {token}"}

    # Construction du contexte
    full_context = "Tu es Klayz, une IA amicale et intelligente.\n\n"
    for msg in history[-5:]:
        role = "Utilisateur" if msg["role"] == "user" else "Klayz"
        full_context += f"{role}: {msg['content']}\n"
    full_context += f"Utilisateur: {prompt}\nKlayz: "

    payload = {
        "inputs": full_context,
        "parameters": {"max_new_tokens": 500, "temperature": 0.7, "do_sample": True}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        result = response.json()
        if isinstance(result, list):
            return result[0].get("generated_text", "").split("Klayz:")[-1].strip()
        return "Désolé, j'ai un petit bug moteur. Réessaie ?"
    except Exception as e:
        return f"Erreur de connexion : {str(e)}"

# ===================== CHAT INPUT =====================
if prompt := st.chat_input("Dis quelque chose à Klayz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown('<span class="typing">Klayz réfléchit...</span>', unsafe_allow_html=True)
        
        response_text = query_klayz(prompt, st.session_state.messages[:-1])
        
        # Effet d'écriture
        full_res = ""
        for char in response_text:
            full_res += char
            placeholder.markdown(full_res + "█")
            time.sleep(0.01)
        placeholder.markdown(response_text)
        
        st.session_state.messages.append({"role": "assistant", "content": response_text})