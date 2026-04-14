import streamlit as st
import requests
import time

# ===================== CONFIGURATION DE LA PAGE =====================
st.set_page_config(
    page_title="Klayz IA",
    page_icon="⚡",
    layout="wide"
)

# Style CSS pour un look futuriste (Sombre et Néon)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stChatMessage { border-radius: 15px; border: 1px solid #1f2937; }
    .stChatInputContainer { padding-bottom: 20px; }
    h1 { color: #00f5ff; text-align: center; font-family: 'Courier New', monospace; }
    .status-text { font-size: 0.8rem; color: #94a3b8; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# LIGNE CORRIGÉE : Utilisation de guillemets simples pour la classe CSS
st.markdown("<h1>⚡ KLAYZ NEURAL INTERFACE</h1>", unsafe_allow_html=True)
st.markdown("<p class='status-text'>Intelligence Artificielle v3.0 • Status: Opérationnel</p>", unsafe_allow_html=True)

# ===================== BARRE LATÉRALE =====================
with st.sidebar:
    st.header("⚙️ Système")
    st.info("Modèle: Zephyr-7B-Beta")
    if st.button("🗑️ Effacer la mémoire", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("Propulsé par Klyz007 & Hugging Face")

# ===================== INITIALISATION DU CHAT =====================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Système activé. Je suis **Klayz**. Comment puis-je t'aider aujourd'hui ?"}
    ]

# Affichage des messages existants
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ===================== MOTEUR DE RÉPONSE (API) =====================
def ask_klayz(prompt):
    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    
    try:
        # Récupération sécurisée du token
        token = st.secrets["HF_TOKEN"]
        headers = {"Authorization": f"Bearer {token}"}
    except:
        return "⚠️ Erreur : Le token HF_TOKEN est manquant dans les Secrets Streamlit."

    # Préparation du texte pour l'IA (Format Zephyr)
    formatted_prompt = f"<|system|>\nTu es Klayz, une IA puissante et amicale.</s>\n<|user|>\n{prompt}</s>\n<|assistant|>\n"
    
    payload = {
        "inputs": formatted_prompt,
        "parameters": {"max_new_tokens": 512, "temperature": 0.7, "return_full_text": False}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=25)
        output = response.json()

        # Si le modèle est en train de charger
        if isinstance(output, dict) and "estimated_time" in output:
            wait_time = int(output['estimated_time'])
            return f"⏳ Mon processeur chauffe... Je serai prêt dans environ {wait_time} secondes. Réessaie dans un instant !"

        # Si on a une réponse valide
        if isinstance(output, list) and len(output) > 0:
            return output[0].get("generated_text", "Je n'ai pas pu générer de texte.")
            
        return "❌ Bug moteur (Erreur API). Réessaie pour voir ?"

    except Exception as e:
        return f"📡 Erreur de connexion : {str(e)}"

# ===================== ZONE DE SAISIE =====================
if user_input := st.chat_input("Envoyez un message à Klayz..."):
    # Ajouter le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Réponse de l'IA
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("*Klayz analyse les données...*")
        
        full_response = ask_klayz(user_input)
        
        # Effet de frappe fluide
        displayed_text = ""
        for char in full_response:
            displayed_text += char
            placeholder.markdown(displayed_text + "▌")
            time.sleep(0.005)
        placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
