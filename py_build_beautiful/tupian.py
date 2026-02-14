from PIL import Image
from collections import Counter

def analyze_border_colors(image_path, depth=40):
    """
    分析图片边缘的颜色一致性
    :param image_path: 图片路径
    :param depth: 扫描边缘向内几层像素（默认扫描最外层和次外层，共2层）
    """
    try:
        print(f"正在分析图片: {image_path} ...")
        img = Image.open(image_path).convert('RGB')
        width, height = img.size
        
        border_pixels = []
        
        # 扫描上下左右四条边，以及向内缩进的 depth 层
        for d in range(depth):
            # 上边 (Top)
            for x in range(d, width - d):
                border_pixels.append(img.getpixel((x, d)))
            # 下边 (Bottom)
            for x in range(d, width - d):
                border_pixels.append(img.getpixel((x, height - 1 - d)))
            # 左边 (Left)
            for y in range(d + 1, height - 1 - d): # 避免角点重复计算
                border_pixels.append(img.getpixel((d, y)))
            # 右边 (Right)
            for y in range(d + 1, height - 1 - d):
                border_pixels.append(img.getpixel((width - 1 - d, y)))
            
        total_pixels = len(border_pixels)
        pixel_counts = Counter(border_pixels)
        unique_colors_count = len(pixel_counts)
        
        # 1. 计算众数 (Mode) - 出现最多的颜色
        most_common = pixel_counts.most_common(1)[0]
        mode_color = most_common[0]
        mode_count = most_common[1]
        mode_percentage = (mode_count / total_pixels) * 100
        
        # 2. 计算均值 (Mean) - 混合后的颜色
        sum_r = sum(p[0] for p in border_pixels)
        sum_g = sum(p[1] for p in border_pixels)
        sum_b = sum(p[2] for p in border_pixels)
        mean_color = (
            int(sum_r / total_pixels), 
            int(sum_g / total_pixels), 
            int(sum_b / total_pixels)
        )
        
        # 辅助函数：转 HEX
        def to_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(*rgb).upper()
            
        print(f"\n--- 📊 分析报告 ---")
        print(f"图片尺寸: {width}x{height}")
        print(f"扫描边缘深度: {depth} px (共扫描 {total_pixels} 个像素)")
        print(f"发现颜色种类: {unique_colors_count} 种")
        
        if unique_colors_count == 1:
            print(f"\n✅ 完美：边缘颜色完全纯净！")
            print(f"👉 请使用: {to_hex(mode_color)}")
        else:
            print(f"\n⚠️ 注意：边缘存在杂色（可能是 JPG 压缩噪点）")
            
            print(f"\n1. 【推荐】众数颜色 (Mode): {to_hex(mode_color)}")
            print(f"   占比: {mode_percentage:.1f}% (它代表了绝大多数背景)")
            
            print(f"\n2. 均值颜色 (Mean): {to_hex(mean_color)}")
            print(f"   (这是混合了所有杂色后的平均值)")
            
            print("\n详细分布 (前5名):")
            for color, count in pixel_counts.most_common(5):
                print(f"   - {to_hex(color)}: 出现 {count} 次")

            # 建议
            if mode_percentage > 90:
                print(f"\n💡 建议：由于众数占比很高 (>90%)，直接使用众数 {to_hex(mode_color)} 即可。")
            else:
                print(f"\n💡 建议：杂色较多，建议使用均值 {to_hex(mean_color)}，或者用 PS 把背景刷纯。")

    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    # 请把这里的文件名换成您实际的图片文件名
    image_file = "assets/封面.png" 
    
    # 也可以检查 splash.png
    # image_file = "assets/splash.png"
    
    analyze_border_colors(image_file, depth=2)