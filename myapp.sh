#!/bin/bash
# myapp.sh

# プロジェクトディレクトリに移動
cd /Wulfric4919/random-Banner/tree/main

# Gunicornを起動
gunicorn --bind 0.0.0.0:8000 app:app
chmod +x myapp.sh
./myapp.sh
