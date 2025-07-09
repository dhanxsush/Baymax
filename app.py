import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Configure Gemini API
genai.configure(api_key="AIzaSyCKK2H8FJxWEnq6oBCAipK5OcitFsdh6TU")  # Replace with your actual key
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")



# Page setup
st.set_page_config(page_title="Baymax: Your Personal Wellness Companion", layout="centered")
st.title("🤖 Baymax: Your Personal Wellness Companion")
st.write("Hello! I'm Baymax, your personal healthcare companion. How can I help you feel better today? 💙")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.mood_history = []

# --- Gemini-based functions ---
def generate_baymax_response(message, history=[]):
    context = "\n".join([f"{sender}: {msg}" for sender, msg in history[-3:]])
    prompt = f"""
You are Baymax, a warm, supportive healthcare companion. Respond empathetically with:
- Emotional validation
- Practical advice or grounding techniques
- Follow-up question or positive encouragement

Use a friendly, short 2-paragraph tone.

Recent context:
{context}

New user message:
{message}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return "I'm having trouble responding right now. Please try again later 💙"

def generate_breathing_tip():
    prompt = "As Baymax, provide a comforting breathing exercise in 1-2 sentences."
    return model.generate_content(prompt).text

def generate_mindfulness_tip():
    prompt = "As Baymax, suggest a calming mindfulness tip in 1-2 sentences."
    return model.generate_content(prompt).text

def generate_mood_summary(mood_history):
    if not mood_history:
        return "You don't have any mood history yet, but I'm here to track how you're feeling over time!"
    
    summary = "\n".join([f"{time.strftime('%m/%d %H:%M')}: {mood}" for mood, time in mood_history[-5:]])
    prompt = f"""As Baymax, analyze this mood history and summarize it supportively in 2 sentences. Be empathetic.

Mood history:
{summary}
"""
    return model.generate_content(prompt).text

# --- UI Interactions ---
user_input = st.text_input("How are you feeling today?")

col1, col2 = st.columns([2, 1])

with col1:
    if st.button("Send") and user_input.strip() != "":
        reply = generate_baymax_response(user_input, st.session_state.chat_history)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", reply))
        
        if any(word in user_input.lower() for word in ["happy", "good", "great"]):
            st.session_state.mood_history.append(("positive", datetime.now()))
        elif any(word in user_input.lower() for word in ["sad", "depressed", "anxious", "angry", "lonely"]):
            st.session_state.mood_history.append(("negative", datetime.now()))

with col2:
    if st.button("🧘 Breathing Tip"):
        tip = generate_breathing_tip()
        st.session_state.chat_history.append(("Bot", tip))
    if st.button("🌿 Mindfulness Tip"):
        tip = generate_mindfulness_tip()
        st.session_state.chat_history.append(("Bot", tip))
    if st.button("📊 Mood History"):
        summary = generate_mood_summary(st.session_state.mood_history)
        st.session_state.chat_history.append(("Bot", summary))

# --- Display chat history ---
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{'🧑 You' if sender == 'You' else '🤖 Baymax'}:** {message}")

# --- Follow-up suggestions ---
if st.session_state.chat_history and "would you like" in st.session_state.chat_history[-1][1].lower():
    st.write("")
    cols = st.columns(3)
    with cols[0]:
        if st.button("Yes, tell me more"):
            st.session_state.chat_history.append(("You", "Yes, tell me more"))
            followup = generate_baymax_response("Yes, tell me more", st.session_state.chat_history)
            st.session_state.chat_history.append(("Bot", followup))
    with cols[1]:
        if st.button("No, thanks"):
            st.session_state.chat_history.append(("You", "No, thanks"))
            st.session_state.chat_history.append(("Bot", "Okay, I'm here if you need me 💙"))
    with cols[2]:
        if st.button("Ask something else"):
            st.session_state.chat_history.append(("You", "I'd like to ask something else"))
