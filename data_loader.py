import os
import re
from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path

# ==========================================
# 1. Data Structures
# ==========================================

@dataclass
class Question:
    id: int                 # 对应文件名中的 sequence_id
    videos: Dict[int, str]  # Key是type_id (0-3), Value是视频文件的相对路径
    
    def is_valid(self) -> bool:
        """
        验证该问题是否完整。
        必须包含所有4个必要阶段的视频 (type_id: 0, 1, 2, 3) 才能返回 True。
        """
        required_types = {0, 1, 2, 3}
        # 检查 required_types 是否是 self.videos.keys() 的子集
        return required_types.issubset(self.videos.keys())

@dataclass
class Topic:
    id: str                    # 文件夹名称 (例如 "topic_family")
    name: str                  # 话题展示名称
    questions: List[Question]  # 该话题下所有 Question 的列表，按 id 升序排列


# ==========================================
# 2. Scanning & Parsing Logic
# ==========================================

def load_topics(assets_dir: str) -> List[Topic]:
    """
    扫描指定目录，构建 Topic 和 Question 对象列表。
    """
    topics: List[Topic] = []
    base_path = Path(assets_dir)

    if not base_path.exists():
        print(f"Warning: Assets directory '{assets_dir}' not found.")
        return []

    # 遍历 assets 下的所有子文件夹 (每个都是一个 Topic)
    for topic_dir in base_path.iterdir():
        if not topic_dir.is_dir():
            continue

        topic_id = topic_dir.name
        # 简单的名称处理：去掉 "topic_" 前缀并大写首字母，提升可读性
        # 例如: "topic_family" -> "Family"
        display_name = topic_id.replace("topic_", "").replace("_", " ").title()

        # 临时存储字典: { sequence_id: { type_id: file_path } }
        temp_questions: Dict[int, Dict[int, str]] = {}

        # 扫描 MP4 文件
        for video_file in topic_dir.glob("*.mp4"):
            # 正则匹配: q{sequence_id}_{type_id}_{desc}.mp4
            # 示例: q1_0_ask.mp4
            match = re.match(r"^q(\d+)_(\d+)_(.+)\.mp4$", video_file.name)

            if match:
                try:
                    seq_id = int(match.group(1))
                    type_id = int(match.group(2))
                    
                    # 关键点：Flet 需要相对路径且使用正斜杠 "/"
                    # Path.as_posix() 会自动处理 Windows 反斜杠问题
                    rel_path = video_file.as_posix()

                    if seq_id not in temp_questions:
                        temp_questions[seq_id] = {}
                    
                    temp_questions[seq_id][type_id] = rel_path

                except ValueError:
                    print(f"[Warn] 解析数字失败: {video_file.name}")
            else:
                print(f"[Warn] 跳过不符合命名规范的文件: {video_file.as_posix()}")

        # 构建并筛选有效的 Question 对象
        valid_questions: List[Question] = []
        
        for seq_id, videos_map in temp_questions.items():
            q = Question(id=seq_id, videos=videos_map)
            if q.is_valid():
                valid_questions.append(q)
            else:
                missing = {0, 1, 2, 3} - set(videos_map.keys())
                print(f"[Warn] Topic '{topic_id}' Question {seq_id} 不完整，缺少阶段: {missing}")

        # 如果该 Topic 下有有效问题，才添加到结果列表
        if valid_questions:
            # 按 id 升序排列
            valid_questions.sort(key=lambda x: x.id)
            topics.append(Topic(
                id=topic_id, 
                name=display_name, 
                questions=valid_questions
            ))

    print(f"数据加载完成: 共加载 {len(topics)} 个话题。")
    return topics


# ==========================================
# 4. Verification (Test Code)
# ==========================================

if __name__ == "__main__":
    # 模拟测试
    print("--- 开始测试 Data Loader ---")
    
    # 假设你的目录结构已经在 assets 中建立
    all_topics = load_topics("assets")

    if all_topics:
        first_topic = all_topics[0]
        print(f"\n检测到 Topic: {first_topic.name} (ID: {first_topic.id})")
        print(f"包含 {len(first_topic.questions)} 个有效问题")

        if first_topic.questions:
            first_q = first_topic.questions[0]
            print(f"\n第一个问题的 ID: {first_q.id}")
            print("视频路径字典 (检查正斜杠和相对路径):")
            for t_id, path in first_q.videos.items():
                print(f"  Type {t_id}: {path}")
            
            # 验证完整性逻辑
            print(f"IsValid: {first_q.is_valid()}")
    else:
        print("\n未找到有效 Topic，请检查 'assets' 文件夹结构是否符合 README 要求。")