# 🚀 WhatsApp Bot Python (Neonize)

WhatsApp Bot yang ringan, cepat, dan hemat resource. Dibangun menggunakan Python dengan library **Neonize** (Go engine). Sangat cocok untuk dideploy di server gratisan seperti **AWS EC2 (Free Tier)**.

## ✨ Fitur
- [x] **Multi-Device Support**: Scan sekali, bot jalan terus.
- [x] **Lightweight**: Menggunakan SQLite untuk sesi.
- [x] **Fast Response**: Berbasis Go-nebula (whatsmeow).
- [x] **Easy Deployment**: Dilengkapi dengan script otomatis untuk Linux/AWS.

## 🛠️ Instalasi Lokal (Windows/Mac)
1. **Clone Repository**:
   ```bash
   git clone <url-repo-anda>
   cd wa-bot
   ```
2. **Instal Library**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Jalankan Bot**:
   ```bash
   python main.py
   ```
4. **Scan QR Code** yang muncul di terminal.

## ☁️ Deployment ke AWS EC2 (Ubuntu)
1. SSH ke instance AWS Anda.
2. Clone repository Anda di server.
3. Berikan izin eksekusi pada script setup:
   ```bash
   chmod +x setup_aws.sh
   ./setup_aws.sh
   ```
4. Jalankan dalam background menggunakan `tmux`:
   ```bash
   tmux new -s wabot
   source venv/bin/activate
   python3 main.py
   ```
   *Tekan `Ctrl+B` lalu `D` untuk keluar dari tmux tanpa mematikan bot.*

## 📂 Struktur File
- `main.py`: Logika utama bot.
- `session.db`: File database sesi (DIBUAT OTOMATIS, JANGAN DI-PUSH).
- `setup_aws.sh`: Script auto-install untuk Linux server.
- `.gitignore`: Melindungi data sensitif agar tidak terupload ke GitHub.

---
**Note**: Jika bot tidak merespon, hapus `session.db` dan scan ulang.
