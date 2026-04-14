import streamlit as st
import requests
import time

# ===================== CONFIGURATION =====================
st.set_page_config(page_title="Klayz IA", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stChatMessage { border-radius: 15px; border: 1px solid #1f2937; }
    h1 { color: #00f5ff; text-align: center; font-family: 'Courier New', monospace; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>⚡ KLAYZ NEURAL INTERFACE</h1>", unsafe_allow_html=True)

# ===================== MOTEUR API CORRIGÉ =====================
def ask_klayz(prompt):
    # L'URL EXACTE DEMANDÉE PAR LE SERVEUR
    API_URL = "https://router.huggingface.co/hf-inference/models/gpt2"
    
    try:
        # Vérification du Token dans les secrets
        token = st.secrets["HF_TOKEN"]
        # On nettoie le token au cas où il y aurait des espaces ou guillemets en trop
        token = token.replace('"', '').replace("'", "").strip()
        headers = {"Authorization": f"Bearer {token}"}
    except Exception as e:
        return f"⚠️ Problème de Secret : {str(e)}"

    payload = {
        "inputs": f"User: {prompt}\nAI:",
        "parameters": {"max_new_tokens": 50, "temperature": 0.7},
        "options": {"wait_for_model": True}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        output = response.json()

        if isinstance(output, list) and len(output) > 0:
            res = output[0].get("generated_text", "")
            return res.split("AI:")[-1].strip()
        
        if isinstance(output, dict) and "error" in output:
            return f"❌ Erreur Serveur : {output['error']}"
            
        return "❌ Format de réponse inconnu."
    except Exception as e:
        return f"📡 Erreur connexion : {str(e)}"

# ===================== INTERFACE CHAT =====================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Système prêt. Adresse IP Router configurée. **Klayz** est en ligne."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Tape ton message ici..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Transmission..."):
            full_response = ask_klayz(user_input)
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
