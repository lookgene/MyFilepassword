#!/usr/bin/env python3
"""
简化的命令行入口脚本
"""

import sys
import os

# 添加当前目录到路径，以便导入模块
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from zip_cracker_cli import main

if __name__ == "__main__":
    main()