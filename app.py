import os
import requests
import streamlit as st

# Konfigurasi halaman Streamlit (Harus paling atas di antara perintah st lainnya)
st.set_page_config(
    page_title="2D Virtual Office AI Agent",
    page_icon="🤖",
    layout="wide"
)

def send_telegram_alert(message):
    """Fungsi lama lu untuk mengirim alert error ke Telegram"""
    try:
        # Mengambil token dan chat ID dari Streamlit Secrets atau Environment
        bot_token = st.secrets.get("TELEGRAM_BOT_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID") or os.environ.get("TELEGRAM_CHAT_ID")
        
        if not bot_token or not chat_id:
            return  # Jangan kirim kalau konfigurasi rahasianya belum terpasang
            
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": f"⚠️ HERMES ALERT:\n{message}"}
        requests.post(url, json=payload, timeout=5)
    except Exception:
        pass # Menghindari infinite loop error jika Telegram gagal dihubungi

def main():
    st.title("🤖 2D Virtual Office AI Agent")
    st.markdown("Selamat datang di panel kontrol Virtual Office Agent berbasis Gemini API & LangChain!")

    # Sidebar untuk info / konfigurasi tambahan
    with st.sidebar:
        st.header("⚙️ Status Sistem")
        st.success("Server Aktif & Siap")
        st.info("Environment: Streamlit Cloud")

    # Area Interaksi Utama (Menggunakan input chat atau form agar tidak jalan otomatis)
    user_input = st.text_input("Ketik perintah atau pesan untuk AI Agent:")
    
    if st.button("Kirim Perintah", type="primary"):
        if user_input:
            with st.spinner("Agent sedang memproses permintaan..."):
                try:
                    # --- GABUNGKAN LOGIKA LAMA LU DI SINI ---
                    # Contoh: Pemanggilan LangChain / Gemini 1.5 Flash
                    # model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=st.secrets["GEMINI_API_KEY"])
                    # response = model.invoke(user_input)
                    
                    # Dummy response sementara untuk testing UI
                    response_text = f"Agent berhasil merespons perintah: '{user_input}'"
                    
                    st.success(response_text)
                    
                except Exception as e:
                    # Jika gagal, fungsi Telegram lama lu langsung mengeksekusi alert
                    error_msg = str(e)
                    send_telegram_alert(f"Agent gagal merespons. Error: {error_msg}")
                    st.error(f"Terjadi kesalahan sistem: {error_msg}")
        else:
            st.warning("Mohon masukkan pesan terlebih dahulu!")

if __name__ == "__main__":
    main()