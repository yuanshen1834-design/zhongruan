"""生成 Android 应用图标（多尺寸 PNG）"""
import struct
import zlib
import os

def create_png(width, height, pixels):
    """从 RGBA 像素数据创建 PNG 文件字节"""
    def chunk(ctype, data):
        c = ctype + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    raw = b''
    for y in range(height):
        raw += b'\x00' + pixels[y * width * 4:(y + 1) * width * 4]
    idat = zlib.compress(raw, 9)
    return sig + chunk(b'IHDR', ihdr) + chunk(b'IDAT', idat) + chunk(b'IEND', b'')

def make_icon_pixels(size):
    """生成指定尺寸的中阮图标像素数据"""
    cx, cy = size // 2, size // 2
    radius = int(size * 0.41)

    pixels = bytearray(size * size * 4)

    for y in range(size):
        for x in range(size):
            idx = (y * size + x) * 4
            dx = x - cx
            dy = y - cy
            dist = (dx * dx + dy * dy) ** 0.5

            if dist > radius + size * 0.02:
                pixels[idx] = 0
                pixels[idx + 1] = 0
                pixels[idx + 2] = 0
                pixels[idx + 3] = 0
            elif dist > radius:
                alpha = max(0, min(255, int((radius + size * 0.02 - dist) / (size * 0.02) * 255)))
                pixels[idx] = 58
                pixels[idx + 1] = 31
                pixels[idx + 2] = 10
                pixels[idx + 3] = alpha
            else:
                nx = dx / radius
                ny = dy / radius
                r = int(138 + 50 * (-nx * 0.3 - ny * 0.3))
                g = int(79 + 30 * (-nx * 0.3 - ny * 0.3))
                b = int(28 + 15 * (-nx * 0.3 - ny * 0.3))

                hole_r = int(size * 0.11)
                hole_dist = (dx * dx + dy * dy) ** 0.5
                if hole_dist < hole_r:
                    r, g, b = 10, 5, 3
                elif hole_dist < hole_r + 2:
                    t = (hole_dist - hole_r) / 2
                    r = int(r * (1 - t) + 10 * t)
                    g = int(g * (1 - t) + 5 * t)
                    b = int(b * (1 - t) + 3 * t)

                # 琴弦
                string_x = [cx - int(size*0.08), cx - int(size*0.03), cx + int(size*0.03), cx + int(size*0.08)]
                sw = max(1, size // 80)
                for sx in string_x:
                    if abs(x - sx) <= sw and hole_dist > hole_r + 2:
                        r, g, b = 212, 168, 67
                        if abs(x - sx) <= 1:
                            r, g, b = 240, 200, 80

                # 琴颈
                neck_w = int(size * 0.1)
                if dy < -radius + int(size*0.04) and abs(dx) < neck_w:
                    r, g, b = 107, 61, 20
                    for sx in string_x:
                        if abs(x - sx) <= sw:
                            r, g, b = 212, 168, 67

                pixels[idx] = max(0, min(255, r))
                pixels[idx + 1] = max(0, min(255, g))
                pixels[idx + 2] = max(0, min(255, b))
                pixels[idx + 3] = 255

    return bytes(pixels)

def main():
    base = r'f:\1W\yinpiao\android-app\app\src\main\res'
    sizes = {
        'mipmap-mdpi': 48,
        'mipmap-hdpi': 72,
        'mipmap-xhdpi': 96,
        'mipmap-xxhdpi': 144,
        'mipmap-xxxhdpi': 192,
    }

    for folder, size in sizes.items():
        dir_path = os.path.join(base, folder)
        os.makedirs(dir_path, exist_ok=True)

        # 方形图标
        square_pixels = make_icon_pixels(size)
        png_data = create_png(size, size, square_pixels)
        with open(os.path.join(dir_path, 'ic_launcher.png'), 'wb') as f:
            f.write(png_data)

        # 圆形图标（简单圆形遮罩）
        round_pixels = bytearray(size * size * 4)
        cx, cy = size // 2, size // 2
        for y in range(size):
            for x in range(size):
                idx = (y * size + x) * 4
                dx = x - cx
                dy = y - cy
                if (dx * dx + dy * dy) ** 0.5 <= size * 0.45:
                    # 复制方形图标的像素
                    round_pixels[idx] = square_pixels[idx]
                    round_pixels[idx + 1] = square_pixels[idx + 1]
                    round_pixels[idx + 2] = square_pixels[idx + 2]
                    round_pixels[idx + 3] = square_pixels[idx + 3]
                else:
                    round_pixels[idx + 3] = 0

        with open(os.path.join(dir_path, 'ic_launcher_round.png'), 'wb') as f:
            f.write(create_png(size, size, bytes(round_pixels)))

        print(f'已生成 {folder} ({size}x{size})')

    print('所有图标生成完成！')

if __name__ == '__main__':
    main()
