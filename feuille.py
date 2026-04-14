import streamlit as st
import requests
import time

# ===================== CONFIGURATION DE LA PAGE =====================
st.set_page_config(page_title="Klayz IA", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stChatMessage { border-radius: 15px; border: 1px solid #1f2937; }
    h1 { color: #00f5ff; text-align: center; font-family: 'Courier New', monospace; }
    .status-text { font-size: 0.8rem; color: #94a3b8; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>⚡ KLAYZ NEURAL INTERFACE</h1>", unsafe_allow_html=True)
st.markdown("<p class='status-text'>v3.3 • Mode Compatibilité Maximale</p>", unsafe_allow_html=True)

# ===================== INITIALISATION DU CHAT =====================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Système activé. Je suis **Klayz**. Prêt à répondre !"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ===================== MOTEUR DE RÉPONSE =====================
def ask_klayz(prompt):
    # Utilisation de GPT-2 : Le modèle le plus compatible au monde sur HF
    API_URL = "https://api-inference.huggingface.co/models/gpt2"
    
    try:
        token = st.secrets["HF_TOKEN"]
        headers = {"Authorization": f"Bearer {token}"}
    except:
        return "⚠️ Erreur : Token manquant dans les Secrets."

    payload = {
        "inputs": f"L'utilisateur demande : {prompt}\nKlayz répond :",
        "parameters": {"max_new_tokens": 100, "temperature": 0.7},
        "options": {"wait_for_model": True}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        output = response.json()

        if isinstance(output, list) and len(output) > 0:
            text = output[0].get("generated_text", "")
            # On nettoie pour ne garder que la réponse après le prompt
            return text.split("Klayz répond :")[-1].strip()
        
        if isinstance(output, dict) and "error" in output:
            return f"❌ Erreur : {output['error']}"
            
        return "❌ Problème de réponse. Réessaye."
    except Exception as e:
        return f"📡 Erreur de connexion : {str(e)}"

# ===================== ZONE DE SAISIE =====================
if user_input := st.chat_input("Dis quelque chose..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ask_klayz(user_input)
        
        displayed_text = ""
        for char in full_response:
            displayed_text += char
            placeholder.markdown(displayed_text + "▌")
            time.sleep(0.01)
        placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
