import base64
from pathlib import Path

from PIL import Image


def generate_logos():
    # Find source PNG in downloads or user uploaded
    downloads = Path(r"C:\Users\User\Downloads")
    cand = [f for f in downloads.glob("*Afrique*") if "neon" in f.name.lower() or "afrique" in f.name.lower()]
    if cand:
        src_path = cand[0]
    else:
        src_path = Path(
            r"C:/Users/User/.gemini/antigravity/brain/8c6ccbc9-5511-49c9-82f8-443790fab289/.user_uploaded/media_1793798339601_cca2f172.jpg"
        )

    print(f"Loading source logo from: {src_path}")
    orig = Image.open(src_path).convert("RGBA")
    w, h = orig.size

    # Create a square canvas to keep aspect ratio centered
    max_dim = max(w, h)
    # Background color from corners of image
    bg_color = (2, 6, 23, 255)  # Deep obsidian dark #020617

    square_img = Image.new("RGBA", (max_dim, max_dim), bg_color)
    offset_x = (max_dim - w) // 2
    offset_y = (max_dim - h) // 2
    square_img.paste(orig, (offset_x, offset_y))

    # Destinations
    dest_dirs = [Path("static/img"), Path("custom/public/assets/img"), Path("gitea_home/custom/public/assets/img")]
    for d in dest_dirs:
        d.mkdir(parents=True, exist_ok=True)

    # 1. High-res 512x512 PNG
    logo_512 = square_img.resize((512, 512), Image.Resampling.LANCZOS)

    # 2. Medium 256x256 PNG
    logo_256 = square_img.resize((256, 256), Image.Resampling.LANCZOS)

    # 3. Small favicon 64x64 and 32x32
    logo_64 = square_img.resize((64, 64), Image.Resampling.LANCZOS)
    logo_32 = square_img.resize((32, 32), Image.Resampling.LANCZOS)

    # Convert 512 to bytes for base64 SVG embedding
    import io

    b512 = io.BytesIO()
    logo_512.save(b512, format="PNG", optimize=True)
    b64_str = base64.b64encode(b512.getvalue()).decode("ascii")

    # Generate crisp SVG embedding the high-resolution logo
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#00e5ff" flood-opacity="0.6"/>
    </filter>
  </defs>
  <rect width="512" height="512" rx="48" fill="#020617"/>
  <image href="data:image/png;base64,{b64_str}" width="512" height="512" filter="url(#neonGlow)"/>
</svg>"""

    # Favicon SVG
    b32 = io.BytesIO()
    logo_64.save(b32, format="PNG", optimize=True)
    b64_fav = base64.b64encode(b32.getvalue()).decode("ascii")
    fav_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="100%" height="100%">
  <rect width="64" height="64" rx="12" fill="#020617"/>
  <image href="data:image/png;base64,{b64_fav}" width="64" height="64"/>
</svg>"""

    for d in dest_dirs:
        # Save PNGs
        logo_512.save(d / "logo.png", format="PNG", optimize=True)
        logo_512.save(d / "bantu-africa-cyber-logo.png", format="PNG", optimize=True)
        logo_256.convert("RGB").save(d / "logo.jpg", format="JPEG", quality=95)
        logo_32.save(d / "favicon.png", format="PNG")
        logo_32.save(d / "favicon.ico", format="ICO")

        # Save SVGs
        with open(d / "logo.svg", "w", encoding="utf-8") as f:
            f.write(svg_content)
        with open(d / "favicon.svg", "w", encoding="utf-8") as f:
            f.write(fav_svg)
        print(f"Generated logo assets in {d}")


if __name__ == "__main__":
    generate_logos()
