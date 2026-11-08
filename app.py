# Tulis atau tempel kode utama app.py di sini
import os
import requests
import streamlit as st

def send_telegram_alert(message):
    # Mengambil token dan chat ID dari environment (atau Streamlit Secrets)
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN") or st.secrets["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ.get("TELEGRAM_CHAT_ID") or st.secrets["TELEGRAM_CHAT_ID"]
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": f"⚠️ HERMES ALERT:\n{message}"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        pass # Hindari loop error

# Contoh implementasi di logic AI Agent:
try:
    # Logic LangChain / Gemini 1.5 Flash berjalan di sini...
    pass
except Exception as e:
    send_telegram_alert(f"Agent gagal merespons. Error: {str(e)}")
    st.error("Terjadi kesalahan sistem. Tim sedang memperbaikinya.")