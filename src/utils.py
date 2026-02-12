"""
通用工具函数模块
包含跨平台路径处理等通用功能
"""

import pathlib
import platform
import os


def get_video_src(raw_path: str) -> str:
    """
    全平台通用的绝对物理路径策略
    处理外部视频文件的路径转换
    
    参数:
        raw_path: 原始路径字符串
        
    返回:
        URI 格式的路径 (file:///...)，这对 Android 的 ExoPlayer 最安全
    """
    # raw_path 已经是绝对路径（来自 data_loader）
    full_path = pathlib.Path(raw_path).resolve()
    # 打印 DEBUG 日志到控制台
    print(f"DEBUG: Target={full_path} | Exists={full_path.exists()}")
    # 返回 URI 格式的路径 (file:///...)，这对 Android 的 ExoPlayer 最安全
    return full_path.as_uri()
