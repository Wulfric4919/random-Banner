#!/bin/bash
# myapp.sh

# プロジェクトディレクトリに移動
cd /path/to/your/project

# Gunicornを起動
gunicorn --bind 0.0.0.0:8080 app:app
