"""
测试 welcome.py 视图的创建
"""
import sys
import os

# 将 src 目录添加到 Python 路径，这样可以使用相对导入
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

import flet as ft
from data_loader import load_topics
from views.welcome import get_welcome_view

def main(page: ft.Page):
    # 加载话题数据
    topics = load_topics("src/assets")
    if not topics:
        print("未找到话题，使用模拟数据")
        from dataclasses import dataclass
        from typing import List
        
        @dataclass
        class Question:
            id: int
            videos: dict
        
        @dataclass
        class Topic:
            id: str
            name: str
            questions: List[Question]
            cover_image_path: str
        
        topics = [
            Topic(
                id="topic_test",
                name="测试话题",
                questions=[],
                cover_image_path="src/assets/topic_huize/cover.png"  # 使用实际存在的图片
            )
        ]
    
    print(f"加载了 {len(topics)} 个话题")
    for topic in topics:
        print(f"话题: {topic.name}, 封面: {topic.cover_image_path}")
    
    async def on_topic_enter(topic):
        print(f"进入话题: {topic.name}")
    # 获取欢迎视图
    view = get_welcome_view(page, topics, on_topic_enter)
    page.views.append(view)
    page.update()

if __name__ == "__main__":
    ft.run(main)
