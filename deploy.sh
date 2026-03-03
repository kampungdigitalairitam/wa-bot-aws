#!/bin/bash
echo "🚀 Memulai Deployment Manual..."
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
pm2 restart wa-bot || pm2 start venv/bin/python --name "wa-bot" -- main.py
pm2 save
echo "✅ Deployment Selesai!"
