import os
import time
import logging
import threading
from dotenv import load_dotenv
from neonize.client import NewClient
from neonize.events import MessageEv, ConnectedEv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("WABot")

class WhatsAppBot:
    def __init__(self, db_path="session.db"):
        self.db_path = db_path
        self.client = NewClient(self.db_path)
        self.setup_events()

    def setup_events(self):
        @self.client.event(ConnectedEv)
        def on_connected(client, event):
            print("\n" + "="*40)
            print("🚀 WHATSAPP CONNECTED SUCCESSFULLY!")
            print("="*40)
            logger.info("WhatsApp Connected successfully!")

        @self.client.event(MessageEv)
        def on_message(client, message):
            try:
                # Robust extraction for neonize versions
                info = getattr(message, "Info", None) or getattr(message, "info", None)
                if not info: return

                source = getattr(info, "MessageSource", None) or getattr(info, "source", None)
                if source:
                    is_from_me = getattr(source, "IsFromMe", False)
                    chat_jid = getattr(source, "Chat", None)
                    sender_jid = getattr(source, "Sender", None)
                else:
                    is_from_me = getattr(info, "IsFromMe", False)
                    chat_jid = getattr(info, "Chat", None)
                    sender_jid = getattr(info, "Sender", None)

                if is_from_me: return

                # Extract content
                text = ""
                m = getattr(message, "Message", None) or getattr(message, "message", None)
                if not m: return

                if hasattr(m, "conversation") and m.conversation:
                    text = m.conversation
                elif hasattr(m, "extendedTextMessage") and m.extendedTextMessage.text:
                    text = m.extendedTextMessage.text
                elif hasattr(m, "imageMessage") and m.imageMessage.caption:
                    text = m.imageMessage.caption
                elif hasattr(m, "videoMessage") and m.videoMessage.caption:
                    text = m.videoMessage.caption

                if not text: return

                print(f"📩 Pesan masuk dari {sender_jid}: {text}")

                # Simple Logic
                cmd = text.strip().lower()
                if cmd in [".ping", "ping", "p"]:
                    print(f"📤 Membalas Pong ke {chat_jid}")
                    self.client.send_message(chat_jid, "Pong! 🏓")
                
                elif cmd in [".menu", "menu", "help"]:
                    help_text = (
                        "*WhatsApp Bot Neon*\n\n"
                        "Daftar Perintah:\n"
                        "1. *.ping* - Cek koneksi\n"
                        "2. *.status* - Cek bot\n"
                        "3. *.id* - Cek JID anda"
                    )
                    self.client.send_message(chat_jid, help_text)
                
                elif cmd in [".status", "status"]:
                    self.client.send_message(chat_jid, "Bot AKTIF! ✨")
                
                elif cmd in [".id", "id"]:
                    self.client.send_message(chat_jid, f"JID Anda: {sender_jid}")

            except Exception as e:
                logger.error(f"Error: {e}")

    def start(self):
        print(f"\n[!] Memulai Bot (Database: {self.db_path})...")
        print("[!] Tekan Ctrl+C untuk berhenti kapan saja.")
        
        # Jalankan connect di background thread agar main thread bisa menangkap Ctrl+C
        bot_thread = threading.Thread(target=self.client.connect, daemon=True)
        bot_thread.start()

        try:
            while True:
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n[!] Berhenti... Sampai jumpa!")
            os._exit(0)

if __name__ == "__main__":
    bot = WhatsAppBot("session.db")
    bot.start()

