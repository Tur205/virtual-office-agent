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
    st.markdown("Selamat datang di panel kontrol Virtual Office Agent (Streaming Mode)!")

    # Sidebar untuk info sistem
    with st.sidebar:
        st.header("⚙️ Status Sistem")
        st.success("Server Aktif & Siap")
        st.info("Model: gemini-3.5-flash-lite")
        st.info("Timeout: 120 Detik")

    # Area Input Chat / Perintah ke AI
    user_input = st.text_input("Ketik perintah atau pesan untuk AI Agent:")
    
    if st.button("Kirim Perintah", type="primary"):
        if user_input:
            # Menggunakan st.write_stream untuk efek streaming teks secara real-time
            def generate_response_stream():
                max_retries = 3
                api_key = st.secrets["GEMINI_API_KEY"]
                
                # Menggunakan endpoint streaming (streamGenerateContent) dengan model gemini-3.5-flash-lite
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:streamGenerateContent?alt=sse&key={api_key}"
                
                headers = {"Content-Type": "application/json"}
                payload = {
                    "contents": [{
                        "parts": [{"text": user_input}]
                    }]
                }
                
                response = None
                for attempt in range(max_retries):
                    try:
                        # Timeout diset 120 detik sesuai permintaan
                        response = requests.post(url, json=payload, headers=headers, stream=True, timeout=120)
                        if response.status_code == 200:
                            break
                        elif attempt < max_retries - 1:
                            time.sleep(2)
                            continue
                    except Exception:
                        if attempt < max_retries - 1:
                            time.sleep(2)
                            continue
                        raise
                
                if not response or response.status_code != 200:
                    error_detail = response.text if response else "Koneksi gagal"
                    raise Exception(f"API Error (Status {response.status_code if response else 'N/A'}): {error_detail}")

                # Membaca respons SSE (Server-Sent Events) secara streaming per chunk
                import json
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith("data: "):
                            json_str = decoded_line[6:]
                            try:
                                chunk_data = json.loads(json_str)
                                if "candidates" in chunk_data:
                                    parts = chunk_data["candidates"][0]["content"]["parts"]
                                    for part in parts:
                                        if "text" in part:
                                            yield part["text"]
                            except json.JSONDecodeError:
                                pass

            try:
                st.subheader("🤖 AI Agent:")
                # Streamlit generator native untuk efek ketikan mengalir
                st.write_stream(generate_response_stream())
                
            except Exception as e:
                error_msg = str(e)
                send_telegram_alert(f"Agent gagal merespons. Error: {error_msg}")
                st.error(f"Terjadi kesalahan sistem: {error_msg}")
        else:
            st.warning("Mohon masukkan pesan terlebih dahulu!")

if __name__ == "__main__":
    main()