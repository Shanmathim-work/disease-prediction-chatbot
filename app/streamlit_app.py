# app/streamlit_app.py
import streamlit as st
import joblib
import numpy as np
import os

st.set_page_config(page_title="Disease Prediction Chatbot", layout="centered")
st.title("Disease Prediction Chatbot — Demo")
st.markdown("**Disclaimer:** This demo is for educational purposes only. Not medical advice.")

MODEL_PATH = os.path.join("..", "models", "tfidf_lr.joblib")
if not os.path.exists(MODEL_PATH):
    # try relative path for when running from project root
    MODEL_PATH = os.path.join("models", "tfidf_lr.joblib")

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

def predict_topk(text, k=3):
    probs = model.predict_proba([text])[0]
    classes = model.classes_
    idx = np.argsort(probs)[::-1][:k]
    return [(classes[i], float(probs[i])) for i in idx]

if 'history' not in st.session_state:
    st.session_state.history = []
st.subheader("🩺 Common Symptoms (click to add)")
common_symptoms = [
    "fever", "cough", "headache", "body ache", "nausea",
    "vomiting", "chest pain", "shortness of breath",
    "burning urination", "frequent urination",
    "rash", "itching", "fatigue"
]

selected = st.multiselect("Select symptoms", common_symptoms)

with st.form("symp_form", clear_on_submit=True):
    user_input = st.text_area(
    "Describe your symptoms (sentence or comma separated)",
    value=", ".join(selected),
    height=120
)
    submitted = st.form_submit_button("Submit")
if submitted and user_input.strip():
    preds = predict_topk(user_input, k=3)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", preds))

# Show last few messages
st.subheader("💬 Chat")

for who, msg in st.session_state.history:
    if who == "You":
        with st.chat_message("user"):
            st.write(msg)
    else:
        with st.chat_message("assistant"):
            st.write("**Possible conditions:**")
            for d, p in msg:
                st.write(f"🔹 **{d}**")
                st.progress(min(int(p * 100), 100))

st.sidebar.header("Demo Controls")
st.sidebar.write("Model:", "TF-IDF + LogisticRegression")
st.sidebar.write("Number of diseases known:", len(model.classes_))
st.sidebar.write("Tips:")
st.sidebar.write("- Try: 'fever, cough, body ache' or 'severe chest pain and sweating'")

st.info("Remember: If the model's suggestion seems serious (e.g., 'Heart Attack'), seek emergency help.")
st.warning(
    "⚠️ This is an AI-based demo system. "
    "If symptoms are severe or persistent, consult a certified doctor immediately."
)