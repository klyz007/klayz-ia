import streamlit as st
import requests
import time

# ===================== CONFIGURATION =====================
st.set_page_config(page_title="Klayz IA", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stChatMessage { border-radius: 15px; border: 1px solid #1f2937; }
    h1 { color: #00f5ff; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>⚡ KLAYZ NEURAL INTERFACE</h1>", unsafe_allow_html=True)

# ===================== MOTEUR API (LLAMA-3) =====================
def ask_klayz(prompt):
    # Changement pour Llama-3-8B : le plus stable en 2026
    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    
    try:
        token = st.secrets["HF_TOKEN"]
        token = token.replace('"', '').replace("'", "").strip()
        headers = {"Authorization": f"Bearer {token}"}
    except:
        return "⚠️ Token manquant dans les Secrets Streamlit."

    # Format de dialogue pour Llama-3
    payload = {
        "inputs": f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
        "parameters": {"max_new_tokens": 256, "temperature": 0.7},
        "options": {"wait_for_model": True}
    }

    try:
        # On repasse sur l'URL classique car Llama-3 est un modèle officiel "Pro"
        response = requests.post(API_URL, headers=headers, json=payload, timeout=40)
        output = response.json()

        if isinstance(output, list) and len(output) > 0:
            return output[0].get("generated_text", "").split("assistant")[-1].strip()
        
        if isinstance(output, dict) and "error" in output:
            # Si Llama-3 dit aussi non, on tente une URL de secours automatique
            return f"❌ Erreur : {output['error']}"
            
        return "❌ Problème de réception."
    except Exception as e:
        return f"📡 Connexion perdue : {str(e)}"

# ===================== INTERFACE =====================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Protocole Llama-3 activé. Je t'écoute."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Tape ton message..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Klayz réfléchit..."):
            full_response = ask_klayz(user_input)
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
