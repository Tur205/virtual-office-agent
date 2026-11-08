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
    """Fungsi alert error ke Telegram milik lu"""
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

    # Area Input Chat / Perintah ke AI
    user_input = st.text_input("Ketik perintah atau pesan untuk AI Agent:")
    
    if st.button("Kirim Perintah", type="primary"):
        if user_input:
            with st.spinner("🤖 Agent sedang berpikir..."):
                try:
                    # Konfigurasi dan pemanggilan Gemini API menggunakan gemini-pro yang stabil
                    api_key = st.secrets["GEMINI_API_KEY"]
                    genai.configure(api_key=api_key)
                    
                    # Menggunakan model gemini-pro agar tidak 404
                    model = genai.GenerativeModel("gemini-pro")
                    response = model.generate_content(user_input)
                    
                    # Menampilkan hasil respons dari AI
                    st.success("🤖 AI Agent:")
                    st.write(response.text)
                    
                except Exception as e:
                    error_msg = str(e)
                    send_telegram_alert(f"Agent gagal merespons. Error: {error_msg}")
                    st.error(f"Terjadi kesalahan sistem: {error_msg}")
        else:
            st.warning("Mohon masukkan pesan terlebih dahulu!")

if __name__ == "__main__":
    main()