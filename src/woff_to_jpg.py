from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
import os

def woff_png(woff_file, output_folder, font_size, image_size):
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 加载字体文件
    font = TTFont(woff_file)
    glyph_set = font.getGlyphSet()
    cmap = font['cmap'].getcmap(3, 1).cmap  # Unicode 映射表

    # 遍历字形并绘制
    for unicode_val, glyph_name in cmap.items():
        try:
            # 创建空白图片
            img = Image.new("RGB", image_size, "white")
            draw = ImageDraw.Draw(img)

            # 使用 FreeTypeFont 加载字形
            temp_font_path = "temp.ttf"
            font.save(temp_font_path)  # 保存临时 TTF 文件
            pil_font = ImageFont.truetype(temp_font_path, font_size)

            # 获取字符并计算位置
            char = chr(unicode_val)
            bbox = draw.textbbox((0, 0), char, font=pil_font)  # 获取边界框
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]       # 宽高
            position = ((image_size[0] - w) // 2, (image_size[1] - h) // 2)

            # 绘制文字
            draw.text(position, char, font=pil_font, fill="black")

            # 保存图片，文件名为 Unicode 编码
            img_name = f"{unicode_val}.jpg"  # 文件名为 Glyph ID
            img_path = os.path.join(output_folder, img_name)
            img.save(img_path)

            print(f"Saved: {img_path}")
        except Exception as e:
            print(f"Failed to render glyph {glyph_name} {unicode_val}: {e}")

    # 清理临时文件
    if os.path.exists(temp_font_path):
        os.remove(temp_font_path)

    print("Finished rendering glyphs.")


if __name__ == "__main__":
    # 配置参数
    _woff_file = "../data/dc027189e0ba4cd.woff2"  # WOFF 文件路径
    _output_folder = "../output/wait_for_identify_images"  # 输出图片文件夹
    _font_size = 120  # 字形绘制大小
    _image_size = (224, 224)  # 图片尺寸
    woff_png(_woff_file, _output_folder, _font_size, _image_size)