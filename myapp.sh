#!/bin/bash
# start.sh

# 必要な場合、仮想環境をアクティブ化
# source venv/bin/activate

# Gunicornを起動
gunicorn --bind 0.0.0.0:8000 app:app
chmod +x myapp.sh
