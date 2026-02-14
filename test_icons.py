#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图标验证脚本
用于验证Windows和Android图标是否符合Flet要求
"""

import os
import sys
from pathlib import Path

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("警告: 未安装PIL库，无法检查图像尺寸。请运行: pip install pillow")

def check_file_exists(filepath, description):
    """检查文件是否存在"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"✅ {description}: 存在 ({size:,} bytes)")
        return True
    else:
        print(f"❌ {description}: 不存在")
        return False

def check_image_dimensions(filepath, platform, min_width, min_height):
    """检查图像尺寸"""
    if not HAS_PIL:
        print(f"   ⚠️  无法检查{platform}图标尺寸 (需要PIL库)")
        return False
    
    try:
        with Image.open(filepath) as img:
            width, height = img.size
            format_name = img.format
            mode = img.mode
            
            print(f"   📏 {platform}图标尺寸: {width}×{height} 像素")
            print(f"   📄 格式: {format_name}, 模式: {mode}")
            
            if width >= min_width and height >= min_height:
                print(f"   ✅ 尺寸符合{platform}要求 (≥{min_width}×{min_height}像素)")
                return True
            else:
                print(f"   ❌ 尺寸不符合{platform}要求 (需要≥{min_width}×{min_height}像素)")
                return False
    except Exception as e:
        print(f"   ❌ 无法读取{platform}图标: {e}")
        return False

def check_flet_config():
    """检查Flet配置文件"""
    config_file = "pyproject.toml"
    if os.path.exists(config_file):
        print(f"✅ Flet配置文件 ({config_file}): 存在")
        
        # 读取配置文件内容
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查关键配置
        checks = [
            ("[tool.flet]", "Flet基础配置"),
            ("[tool.flet.android]", "Android配置"),
            ("[tool.flet.windows]", "Windows配置"),
            ("bundle_id", "应用标识符"),
            ("product = \"公公的留声机\"", "应用名称")
        ]
        
        for key, description in checks:
            if key in content:
                print(f"   ✅ {description}: 已配置")
            else:
                print(f"   ⚠️  {description}: 未找到")
        
        return True
    else:
        print(f"❌ Flet配置文件 ({config_file}): 不存在")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("Flet应用图标验证工具")
    print("=" * 60)
    
    # 设置路径
    assets_dir = Path("src/assets")
    
    print(f"\n📁 资源目录: {assets_dir.absolute()}")
    
    # 检查目录是否存在
    if not assets_dir.exists():
        print(f"❌ 资源目录不存在: {assets_dir}")
        return 1
    
    print(f"✅ 资源目录存在")
    
    # 定义要检查的文件
    files_to_check = [
        {
            "filename": "icon_android.png",
            "description": "Android应用图标",
            "platform": "Android",
            "min_width": 192,
            "min_height": 192
        },
        {
            "filename": "icon_windows.png", 
            "description": "Windows应用图标",
            "platform": "Windows",
            "min_width": 256,
            "min_height": 256
        },
        {
            "filename": "splash.png",
            "description": "启动画面",
            "platform": "通用",
            "min_width": 0,
            "min_height": 0
        }
    ]
    
    # 检查所有文件
    all_files_ok = True
    for file_info in files_to_check:
        filepath = assets_dir / file_info["filename"]
        
        print(f"\n🔍 检查: {file_info['description']}")
        print(f"   📍 路径: {filepath}")
        
        # 检查文件是否存在
        exists = check_file_exists(filepath, file_info["description"])
        
        if exists and file_info["min_width"] > 0 and file_info["min_height"] > 0:
            # 检查图像尺寸
            dimensions_ok = check_image_dimensions(
                filepath, 
                file_info["platform"],
                file_info["min_width"],
                file_info["min_height"]
            )
            if not dimensions_ok:
                all_files_ok = False
        elif not exists:
            all_files_ok = False
    
    # 检查Flet配置
    print(f"\n🔧 检查Flet配置:")
    config_ok = check_flet_config()
    
    # 总结
    print(f"\n" + "=" * 60)
    print("验证结果总结:")
    print("=" * 60)
    
    if all_files_ok and config_ok:
        print("🎉 所有检查通过！图标和配置符合Flet要求。")
        print("\n下一步建议:")
        print("1. 运行 'flet build windows' 测试Windows构建")
        print("2. 运行 'flet build android' 测试Android构建")
        print("3. 检查构建输出中的图标显示")
        return 0
    else:
        print("⚠️  发现一些问题需要修复:")
        if not all_files_ok:
            print("   • 图标文件缺失或尺寸不符合要求")
        if not config_ok:
            print("   • Flet配置不完整")
        print("\n建议:")
        print("1. 确保所有图标文件存在于 src/assets/ 目录")
        print("2. 检查图标尺寸是否符合Flet要求")
        print("3. 验证 pyproject.toml 配置")
        return 1

if __name__ == "__main__":
    sys.exit(main())