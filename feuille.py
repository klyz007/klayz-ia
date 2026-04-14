import streamlit as st
import requests
import time

# ===================== CONFIGURATION PAGE =====================
st.set_page_config(page_title="Klayz IA", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stChatMessage { border-radius: 15px; border: 1px solid #1f2937; margin-bottom: 10px; }
    h1 { color: #00f5ff; text-align: center; font-family: 'Courier New', monospace; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>⚡ KLAYZ NEURAL INTERFACE</h1>", unsafe_allow_html=True)

# ===================== FONCTION API (QWEN 2.5 - ACCÈS LIBRE) =====================
def ask_klayz(prompt):
    # Ce modèle est en accès LIBRE : pas de formulaire Meta !
    API_URL = "https://router.huggingface.co/hf-inference/models/Qwen/Qwen2.5-7B-Instruct"
    
    try:
        token = st.secrets["HF_TOKEN"]
        token = token.replace('"', '').replace("'", "").strip()
        headers = {"Authorization": f"Bearer {token}"}
    except:
        return "⚠️ Erreur : Token absent des Secrets Streamlit."

    payload = {
        "inputs": f"<|im_start|>system\nTu es Klayz, une IA amicale. Réponds toujours en français.<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n",
        "parameters": {"max_new_tokens": 512, "temperature": 0.7},
        "options": {"wait_for_model": True}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=40)
        output = response.json()
        
        if isinstance(output, list) and len(output) > 0:
            full_text = output[0].get("generated_text", "")
            # On nettoie pour n'afficher que la réponse
            return full_text.split("assistant\n")[-1].strip()
        
        if isinstance(output, dict) and "error" in output:
            return f"❌ Erreur Serveur : {output['error']}"
            
        return "❌ Problème de réponse."
    except Exception as e:
        return f"📡 Erreur : {str(e)}"

# ===================== INTERFACE CHAT =====================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Système débloqué. **Klayz** (vQwen) est prêt et sans licence Meta !"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ta question pour Klayz..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("⚡ *Liaison neuronale...*")
        
        full_response = ask_klayz(user_input)
        
        # Affichage fluide
        displayed_text = ""
        for char in full_response:
            displayed_text += char
            placeholder.markdown(displayed_text + "▌")
            time.sleep(0.005)
        placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
