from PIL import Image, ImageSequence, ImageDraw, ImageFilter

def fade_gif_edges():
    # --- 配置区域 ---
    input_gif = "assets/splash_anim_source.gif"  # 您的原始 AI GIF 路径
    output_gif = "assets/splash_anim_fixed.gif"  # 输出的完美 GIF 路径
    
    # 想要融合的目标背景色 (这里选纯白，配合您分析出的 Mode)
    # 如果您想用之前的米色，就改成 "#F6F1DE"
    TARGET_COLOR = "#F6F1DE" 
    
    # 边缘羽化强度 (0.0 - 1.0)
    # 0.1 表示边缘 10% 的区域会发生渐变，数值越大过渡越柔和
    FADE_PCT = 0.15 
    # ----------------
    
    try:
        print(f"正在处理 GIF: {input_gif} ...")
        im = Image.open(input_gif)
        
        frames = []
        width, height = im.size
        
        # 1. 创建一个通用的“羽化遮罩” (Alpha Mask)
        # 中心是黑(不透明)，边缘是白(透明) -> 稍后反转使用
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        # 计算羽化区域
        fade_pixels = int(min(width, height) * FADE_PCT)
        
        # 画一个实心矩形在中间
        left, top = fade_pixels, fade_pixels
        right, bottom = width - fade_pixels, height - fade_pixels
        draw.rectangle((left, top, right, bottom), fill=255)
        
        # 高斯模糊，制造柔和过渡
        mask = mask.filter(ImageFilter.GaussianBlur(radius=fade_pixels / 2))
        
        # 2. 处理每一帧
        for frame in ImageSequence.Iterator(im):
            frame = frame.convert("RGBA")
            
            # 创建一个纯色底图
            bg = Image.new("RGBA", (width, height), TARGET_COLOR)
            
            # 使用遮罩将原图合成到底图上
            # 遮罩白色部分显示原图，黑色部分显示背景色
            composite = Image.composite(frame, bg, mask)
            
            # 转回 RGB (GIF 不支持半透明，必须是实色)
            frames.append(composite.convert("RGB").convert("P", palette=Image.ADAPTIVE))

        # 3. 保存新 GIF
        frames[0].save(
            output_gif,
            save_all=True,
            append_images=frames[1:],
            optimize=False,
            duration=im.info.get('duration', 100),
            loop=0
        )
        
        print(f"✅ 成功！已生成边缘净化的 GIF: {output_gif}")
        print(f"👉 请在 views/splash.py 中使用这个新文件。")
        print(f"👉 记得把 pyproject.toml 里的 splash_color 设为 {TARGET_COLOR}")

    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    fade_gif_edges()