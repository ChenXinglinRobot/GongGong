import os

def create_empty_files():
    base_dir = "assets"
    
    # 主题和文件列表
    topics = {
        "topic_huize": [
            "q1_0_ask_snack.txt",
            "q1_1_repeat_snack.txt", 
            "q1_2_praise_snack.txt",
            "q1_3_guide_snack.txt",
            "q2_0_ask_people.txt",
            "q2_1_repeat_people.txt",
            "q2_2_praise_people.txt",
            "q2_3_guide_people.txt"
        ],
        "topic_naming": [
            "q1_0_ask_name.txt",
            "q1_1_repeat_name.txt",
            "q1_2_praise_name.txt",
            "q1_3_guide_name.txt",
            "q2_0_ask_work.txt",
            "q2_1_repeat_work.txt",
            "q2_2_praise_work.txt",
            "q2_3_guide_work.txt"
        ]
    }
    
    for topic, files in topics.items():
        topic_dir = os.path.join(base_dir, topic)
        os.makedirs(topic_dir, exist_ok=True)
        print(f"创建目录: {topic_dir}")
        
        for filename in files:
            file_path = os.path.join(topic_dir, filename)
            # 创建空文件
            open(file_path, 'w').close()
            print(f"  创建文件: {filename}")
        
        print()  # 空行分隔不同主题
    
    print("=" * 50)
    print(f"完成！已创建 {len(topics)} 个主题的空文件")
    print(f"位置: {os.path.abspath(base_dir)}")

if __name__ == "__main__":
    print("正在创建空文件结构...")
    print("=" * 50)
    create_empty_files()