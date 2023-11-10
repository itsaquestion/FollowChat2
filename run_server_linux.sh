#!/bin/bash

# 检查是否在虚拟环境中
if [[ -z "$VIRTUAL_ENV" ]]; then
  echo "Not in a virtual environment, activating..."
  
  # 激活虚拟环境; 适应你的实际路径
  source venv/bin/activate
fi

# 在后台运行 waitress-serve
echo "Starting waitress-serve in the background..."
nohup waitress-serve --listen=127.0.0.1:8001 app:app &
