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

st.markdown("<h1>⚡ KLAYZ NEURAL INTERFACE</h1>", unsafe_allow_html=True)
st.markdown("<p class='status-text'>Intelligence Artificielle v3.2 • Status: Opérationnel (Mistral Mode)</p>", unsafe_allow_html=True)

# ===================== BARRE LATÉRALE =====================
with st.sidebar:
    st.header("⚙️ Système")
    st.info("Modèle: Mistral-7B-v0.3")
    if st.button("🗑️ Effacer la mémoire", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("Propulsé par Klyz007 & Hugging Face")

# ===================== INITIALISATION DU CHAT =====================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Système activé. Je suis **Klayz**, ton IA personnelle. Comment puis-je t'aider ?"}
    ]

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ===================== MOTEUR DE RÉPONSE (API) =====================
def ask_klayz(prompt):
    # Changement pour Mistral-7B-v0.3 (Mieux supporté par le nouveau Router)
    API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.3"
    
    try:
        token = st.secrets["HF_TOKEN"]
        headers = {"Authorization": f"Bearer {token}"}
    except:
        return "⚠️ Erreur : Le token HF_TOKEN est manquant dans les Secrets Streamlit."

    # Format de prompt spécifique à Mistral
    formatted_prompt = f"<s>[INST] Tu es Klayz, une IA puissante, amicale et concise. Réponds en français. {prompt} [/INST]"
    
    payload = {
        "inputs": formatted_prompt,
        "parameters": {
            "max_new_tokens": 512, 
            "temperature": 0.7,
            "return_full_text": False
        },
        "options": {"wait_for_model": True}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        output = response.json()

        # Si on reçoit une liste (succès)
        if isinstance(output, list) and len(output) > 0:
            return output[0].get("generated_text", "Je n'ai pas pu générer de texte.")
        
        # Gestion des erreurs renvoyées par le dictionnaire
        if isinstance(output, dict) and "error" in output:
            if "loading" in output["error"].lower():
                return "⏳ Mes circuits chauffent... Le modèle est en cours de chargement. Réessaie dans 20 secondes !"
            return f"❌ Erreur IA : {output['error']}"
            
        return "❌ Le moteur ne répond pas. Réessaie dans un instant ?"

    except Exception as e:
        return f"📡 Erreur de connexion : {str(e)}"

# ===================== ZONE DE SAISIE =====================
if user_input := st.chat_input("Envoyez un message à Klayz..."):
    # Ajouter le message utilisateur
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Réponse de l'IA
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("*Klayz analyse les données...*")
        
        full_response = ask_klayz(user_input)
        
        # Effet de frappe (Typing effect)
        displayed_text = ""
        for char in full_response:
            displayed_text += char
            placeholder.markdown(displayed_text + "▌")
            time.sleep(0.005)
        placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
