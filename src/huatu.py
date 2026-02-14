from PIL import Image

def generate_white_png(width, height, save_path, color="#F6F1DE"):
    """
    生成指定尺寸和颜色的纯色PNG图片
    :param width: 图片宽度（像素）
    :param height: 图片高度（像素）
    :param save_path: 保存路径（如 "assets/splash.png"）
    :param color: 颜色值（默认纯白色 #FFFFFF）
    """
    try:
        # 1. 创建新的RGB图片画布，背景填充指定颜色
        # mode="RGB" 表示RGB色彩模式，(width, height)是尺寸，color是填充色
        img = Image.new(mode="RGB", size=(width, height), color=color)
        
        # 2. 保存图片为PNG格式
        img.save(save_path, format="PNG")
        
        print(f"✅ 纯白PNG图片已成功生成！")
        print(f"📁 保存路径：{save_path}")
        print(f"📐 图片尺寸：{width}×{height} 像素")
        print(f"🎨 颜色值：{color}")
        
    except Exception as e:
        print(f"❌ 生成失败：{str(e)}")

# ===================== 自定义参数（根据你的需求修改）=====================
if __name__ == "__main__":
    # 启动图尺寸（可根据目标平台调整，比如iOS：1242×2688，Android：1080×2400）
    SPLASH_WIDTH = 1080    # 宽度
    SPLASH_HEIGHT = 1080   # 高度
    # 保存路径（建议直接保存到assets目录，和你之前的路径一致）
    SAVE_PATH = "assets/splash.png"
    
    # 调用函数生成纯白PNG
    generate_white_png(
        width=SPLASH_WIDTH,
        height=SPLASH_HEIGHT,
        save_path=SAVE_PATH
    )