import os
import time
import logging
import threading
from dotenv import load_dotenv
from neonize.client import NewClient
from neonize.events import MessageEv, ConnectedEv
from neonize.utils import build_jid

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

                # OWNER RESTRICTION (Only listen to specific IDs/Numbers)
                # Jika bot tidak merespon, lihat ID di terminal dan masukkan di sini
                OWNERS = ["6282281488763", "32453225893992", "100326308864187"]
                sender_str = str(sender_jid)
                
                # Check if any owner ID is present in the sender string
                is_owner = any(owner in sender_str for owner in OWNERS)
                
                if not is_owner:
                    print(f"⚠️ Pesan diabaikan (Bukan Owner). ID Pengirim: {sender_str}")
                    return

                # Extract content (Robust extraction for neonize versions)
                text = ""
                m = getattr(message, "Message", None) or getattr(message, "message", None)
                if m:
                    # Priority order for extraction
                    if hasattr(m, "conversation") and m.conversation:
                        text = m.conversation
                    elif hasattr(m, "extendedTextMessage") and m.extendedTextMessage.text:
                        text = m.extendedTextMessage.text
                    elif hasattr(m, "imageMessage") and m.imageMessage.caption:
                        text = m.imageMessage.caption
                    elif hasattr(m, "videoMessage") and m.videoMessage.caption:
                        text = m.videoMessage.caption
                    # Fallback for dynamic fields
                    elif hasattr(m, "ListFields"):
                        for field, value in m.ListFields():
                            if field.name in ["conversation", "text"]:
                                text = value
                                break

                if not text: return
                raw_text = text.strip()
                cmd = raw_text.lower()

                print(f"📩 Pesan masuk dari Owner ({sender_str}): '{raw_text[:50]}...'")

                # 1. COMMAND: Request Template
                if cmd == "#kirim":
                    template = (
                        "*📦 TEMPLATE KIRIM PESAN*\n\n"
                        "no: 628xxx\n"
                        "pesan: Isi pesan anda di sini\n"
                        "jumlah: 1\n"
                        "delay: 5"
                    )
                    self.client.send_message(chat_jid, template)
                    return

                # 2. LOGIC: Handle filled template (Flexible detection)
                if "no:" in cmd and "pesan:" in cmd:
                    try:
                        data = {}
                        for line in raw_text.split("\n"):
                            if ":" in line:
                                k, v = line.split(":", 1)
                                data[k.strip().lower()] = v.strip()
                        
                        targets_raw = data.get("no", "")
                        # Mendukung pemisah koma atau titik koma untuk banyak nomor
                        target_list = [t.strip().replace("+", "").replace(" ", "").replace("-", "") for t in targets_raw.replace(";", ",").split(",") if t.strip()]
                        msg = data.get("pesan", "")
                        count = int(data.get("jumlah", 1))
                        delay = int(data.get("delay", 5))

                        if not target_list or not msg:
                            self.client.send_message(chat_jid, "❌ Gagal: Nomor atau Pesan tidak valid.")
                            return

                        num_targets = len(target_list)
                        self.client.send_message(chat_jid, f"⏳ Memulai blast ke {num_targets} tujuan...\n(Harap tunggu jika bot sedang sync riwayat)")

                        for idx, target in enumerate(target_list):
                            dest_jid = build_jid(f"{target}@s.whatsapp.net") if "@" not in target else build_jid(target)
                            print(f"⏳ Process {idx+1}/{num_targets}: {target}")
                            
                            for i in range(count):
                                max_retries = 3
                                for attempt in range(max_retries):
                                    try:
                                        self.client.send_message(dest_jid, msg)
                                        if i < count - 1: time.sleep(delay)
                                        break # Sukses, lanjut ke pesan berikutnya
                                    except Exception as send_err:
                                        err_str = str(send_err).lower()
                                        logger.error(f"Error [{target}] msg {i+1} (Attempt {attempt+1}): {send_err}")
                                        
                                        if "timeout" in err_str or "device list" in err_str:
                                            if attempt < max_retries - 1:
                                                print(f"⚠️ {target} Timeout. Menunggu 10 detik (History Sync sedang sibuk)...")
                                                time.sleep(10)
                                                continue
                                        
                                        # Jika gagal setelah retry atau error bukan timeout
                                        try: self.client.send_message(chat_jid, f"⚠️ Gagal ke {target} (Pesan ke-{i+1}): {str(send_err)}")
                                        except: pass
                                        break
                            
                            # Jeda antar nomor tujuan agar tidak terdeteksi spam
                            if idx < num_targets - 1:
                                time.sleep(2)
                        
                        self.client.send_message(chat_jid, f"✅ Blast selesai ke {num_targets} tujuan!")

                    except Exception as e:
                        logger.error(f"Blast Error: {e}")
                        self.client.send_message(chat_jid, f"❌ Terjadi kesalahan: {str(e)}")
                    return

                # 3. OTHER COMMANDS
                if cmd in [".ping", "ping", "p"]:
                    print(f"📤 Membalas Pong ke {chat_jid}")
                    self.client.send_message(chat_jid, "Pong! 🏓")
                
                elif cmd in [".menu", "menu", "help"]:
                    help_text = (
                        "*WhatsApp Bot Neon*\n\n"
                        "Daftar Perintah:\n"
                        "1. *.ping* - Cek koneksi\n"
                        "2. *.status* - Cek bot\n"
                        "3. *.id* - Cek JID anda\n"
                        "4. *kamu siapa* - Tentang Pembuat"
                    )
                    self.client.send_message(chat_jid, help_text)
                
                elif cmd in [".status", "status"]:
                    self.client.send_message(chat_jid, "Bot AKTIF! ✨")
                
                elif cmd in [".id", "id"]:
                    self.client.send_message(chat_jid, f"JID Anda: {sender_jid}")
                
                elif "kamu siapa" in cmd:
                    self.client.send_message(chat_jid, "Saya dibuat Oleh Irpansyah")

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

