import os
import requests
import streamlit as st
import google.generativeai as genai

# Konfigurasi halaman Streamlit (Wajib di baris paling atas)
st.set_page_config(
    page_title="2D Virtual Office AI Agent",
    page_icon="🤖",
    layout="wide"
)

def send_telegram_alert(message):
    """Fungsi alert error ke Telegram"""
    try:
        bot_token = st.secrets.get("TELEGRAM_BOT_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID") or os.environ.get("TELEGRAM_CHAT_ID")
        
        if not bot_token or not chat_id:
            return  
            
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": f"⚠️ HERMES ALERT:\n{message}"}
        requests.post(url, json=payload, timeout=5)
    except Exception:
        pass 

def main():
    st.title("🤖 2D Virtual Office AI Agent")
    st.markdown("Selamat datang di panel kontrol Virtual Office Agent!")

    # Sidebar untuk info sistem
    with st.sidebar:
        st.header("⚙️ Status Sistem")
        st.success("Server Aktif & Siap")
        st.info("Environment: Streamlit Cloud / Local")
        if st.button("🗑️ Hapus Riwayat Chat"):
            st.session_state.messages = []
            st.rerun()

    # Ambil API Key secara aman (mencoba dari Secrets lalu Env Variable)
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

    if not api_key:
        st.error("⚠️ GEMINI_API_KEY tidak ditemukan! Harap masukkan di Streamlit Secrets atau Environment Variable.")
        st.stop()

    # Inisialisasi model Gemini
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        error_msg = f"Gagal inisialisasi SDK Gemini: {e}"
        send_telegram_alert(error_msg)
        st.error(error_msg)
        return

    # Inisialisasi riwayat chat di Session State
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Tampilkan riwayat chat di UI
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input Chat Kompatibel Streamlit Terbaru
    if prompt := st.chat_input("Ketik perintah atau pesan untuk AI Agent..."):
        # 1. Tampilkan pesan user
        st.chat_message("user").markdown(prompt)
        
        # 2. Format riwayat percakapan untuk SDK Gemini
        formatted_history = []
        for m in st.session_state.messages:
            role = "user" if m["role"] == "user" else "model"
            formatted_history.append({"role": role, "parts": [m["content"]]})

        # 3. Kirim ke Gemini API
        with st.chat_message("assistant"):
            with st.spinner("🤖 Agent sedang berpikir..."):
                try:
                    chat = model.start_chat(history=formatted_history)
                    response = chat.send_message(prompt)
                    reply_text = response.text

                    # Tampilkan balasan
                    st.markdown(reply_text)
                    
                    # Simpan ke session state
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    st.session_state.messages.append({"role": "assistant", "content": reply_text})

                except Exception as e:
                    error_msg = str(e)
                    send_telegram_alert(f"Agent gagal merespons. Error: {error_msg}")
                    st.error(f"Terjadi kesalahan sistem: {error_msg}")

if __name__ == "__main__":
    main()