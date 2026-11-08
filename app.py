import os
import time
import requests
import streamlit as st

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
            with st.spinner("🤖 Agent sedang menghubungi server Google (Auto-retry aktif)..."):
                try:
                    api_key = st.secrets["GEMINI_API_KEY"]
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
                    
                    headers = {"Content-Type": "application/json"}
                    payload = {
                        "contents": [{
                            "parts": [{"text": user_input}]
                        }]
                    }
                    
                    # Mekanisme Auto-Retry (Mencoba hingga 3 kali jika server overload)
                    max_retries = 3
                    res_data = None
                    
                    for attempt in range(max_retries):
                        response = requests.post(url, json=payload, headers=headers, timeout=60)
                        res_data = response.json()
                        
                        # Jika sukses atau error bukan karena high demand, hentikan looping
                        if "candidates" in res_data or "error" not in res_data:
                            break
                        
                        error_msg_check = res_data.get("error", {}).get("message", "")
                        if "high demand" in error_msg_check.lower() and attempt < max_retries - 1:
                            time.sleep(2) # Tunggu 2 detik sebelum mencoba ulang
                            continue
                        break
                    
                    # Ambil teks balasan dari struktur JSON Google API
                    if "candidates" in res_data:
                        reply_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
                        st.success("🤖 AI Agent:")
                        st.write(reply_text)
                    else:
                        error_detail = res_data.get("error", {}).get("message", "Server Google sedang sibuk")
                        raise Exception(f"API Error: {error_detail}")
                    
                except Exception as e:
                    error_msg = str(e)
                    send_telegram_alert(f"Agent gagal merespons. Error: {error_msg}")
                    st.error(f"Terjadi kesalahan sistem: {error_msg}")
        else:
            st.warning("Mohon masukkan pesan terlebih dahulu!")

if __name__ == "__main__":
    main()