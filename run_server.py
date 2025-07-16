#!/usr/bin/env python3
"""
StealthMole MCP Server 실행 스크립트
"""

import os
import sys

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 서버 실행
from src.server import main

if __name__ == "__main__":
    main()
