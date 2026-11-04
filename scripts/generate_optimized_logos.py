import base64
import io
import os
from pathlib import Path
from PIL import Image

def generate_logos():
    src_path = Path(r"C:/Users/User/.gemini/antigravity/brain/8c6ccbc9-5511-49c9-82f8-443790fab289/.user_uploaded/media_1793831090054_560a1ebf.png")
    if not src_path.exists():
        raise FileNotFoundError(f"Source logo not found at {src_path}")

    print(f"Loading transparent source logo from: {src_path}")
    orig = Image.open(src_path).convert("RGBA")
    w, h = orig.size

    # Create a square transparent canvas to keep aspect ratio centered
    max_dim = max(w, h)
    transparent_bg = (0, 0, 0, 0)

    square_img = Image.new("RGBA", (max_dim, max_dim), transparent_bg)
    offset_x = (max_dim - w) // 2
    offset_y = (max_dim - h) // 2
    square_img.paste(orig, (offset_x, offset_y), orig)

    dest_dirs = [
        Path("static/img"),
        Path("custom/public/assets/img"),
        Path("gitea_home/custom/public/assets/img"),
    ]
    for d in dest_dirs:
        d.mkdir(parents=True, exist_ok=True)

    # 1. High-res 512x512 PNG transparent
    logo_512 = square_img.resize((512, 512), Image.Resampling.LANCZOS)

    # 2. Medium 256x256 PNG transparent
    logo_256 = square_img.resize((256, 256), Image.Resampling.LANCZOS)

    # 3. Small favicon 64x64 and 32x32 transparent
    logo_64 = square_img.resize((64, 64), Image.Resampling.LANCZOS)
    logo_32 = square_img.resize((32, 32), Image.Resampling.LANCZOS)

    # Convert 512 to bytes for base64 SVG embedding
    b512 = io.BytesIO()
    logo_512.save(b512, format="PNG", optimize=True)
    b64_str = base64.b64encode(b512.getvalue()).decode("ascii")

    # SVG TRANSPARENT - AUCUN ARRIERE-PLAN (ni rect, ni fond colore)
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#00e5ff" flood-opacity="0.5"/>
    </filter>
  </defs>
  <image href="data:image/png;base64,{b64_str}" width="512" height="512" filter="url(#neonGlow)"/>
</svg>"""

    # Favicon SVG TRANSPARENT
    b32 = io.BytesIO()
    logo_64.save(b32, format="PNG", optimize=True)
    b64_fav = base64.b64encode(b32.getvalue()).decode("ascii")
    fav_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="100%" height="100%">
  <image href="data:image/png;base64,{b64_fav}" width="64" height="64"/>
</svg>"""

    for d in dest_dirs:
        # Save PNGs transparents
        logo_512.save(d / "logo.png", format="PNG", optimize=True)
        logo_512.save(d / "bantu-africa-cyber-logo.png", format="PNG", optimize=True)
        # Pour logo.jpg si requis par d'anciens endpoints
        logo_256.convert("RGB").save(d / "logo.jpg", format="JPEG", quality=95)
        logo_32.save(d / "favicon.png", format="PNG")
        logo_32.save(d / "favicon.ico", format="ICO")

        # Save SVGs sans arriere plan
        with open(d / "logo.svg", "w", encoding="utf-8") as f:
            f.write(svg_content)
        with open(d / "favicon.svg", "w", encoding="utf-8") as f:
            f.write(fav_svg)
        print(f"Generated transparent logo assets in {d}")

if __name__ == "__main__":
    generate_logos()
