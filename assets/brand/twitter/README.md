# stray — black & white logo assets (Twitter / X)

The mark is `▛` — three squares in formation (upper-left, upper-right, lower-left) and a fourth,
smaller one that has strayed to the lower-right corner. Same geometry as
`src/stray/web/favicon.svg` and `plugin/assets/icon.svg`, recoloured to pure
black/white. Wordmark is set in the site's `--mono` stack (SF Mono, 700).

| File | Size | Use |
|---|---|---|
| `avatar-dark-400.png` | 400×400 | **Profile picture** (white ▛ on black) |
| `avatar-light-400.png` | 400×400 | Profile picture, light |
| `avatar-dark.png` / `avatar-light.png` | 512×512 | Same, higher-res |
| `avatar-dark.svg` / `avatar-light.svg` | vector | Source; re-render at any size |
| `banner-dark.png` | 1500×500 | **Header** (white on black) |
| `banner-light.png` | 1500×500 | Header, light |
| `wordmark-white.png` / `wordmark-black.png` | 1400×440, transparent | Lockup for slides, video end-cards |
| `mark-white.svg` / `mark-black.svg` | vector, transparent | Mark alone |

## Notes

- **Avatars are safe in the circular crop.** The mark is inset so its corners
  sit at ~80% of the crop radius — nothing clips.
- **The banner mirrors the README hero** (`docs/assets/stray-hero.png`): the same
  pill lockup, the same `Geist Pixel` headline set to "OpenRouter for agent
  tools", and a `DM Mono` kicker underneath — recoloured to pure black/white.
  Both webfonts load from Google Fonts at render time.
- **Banner content is centred and vertically tight** (~240px tall), so it
  survives X's mobile top/bottom crop and the avatar that overlaps bottom-left.
- Wordmark PNGs are 2× with a real alpha channel — drop them on any background.
- Colours are pure `#000000` / `#ffffff`. The brand colour set (clay `#e0703f`
  on `#211d16`) lives in `src/stray/web/index.html`; these are the mono cut.

Regenerate the PNGs from the SVGs with headless Chrome
(`--headless --window-size=W,H --screenshot=out.png file://…`) — the repo has
no rasteriser installed. For flat geometry like `avatar-dark.svg` a few lines of
Pillow are exact and need no browser:

```bash
uv run --with pillow --no-project python -c "
from PIL import Image, ImageDraw
S=1024; k=S/512                      # every number below is in the 512 viewBox
img=Image.new('RGBA',(S,S),(0,0,0,0)); d=ImageDraw.Draw(img)
d.rounded_rectangle([0,0,S-1,S-1], radius=int(112*k), fill=(0,0,0,255))
for x,y,w,r in ((111,111,140.5,20),(260.5,111,140.5,20),(111,260.5,140.5,20),(331,331,70,14)):
    d.rounded_rectangle([x*k,y*k,(x+w)*k-1,(y+w)*k-1], radius=int(r*k), fill='white')
img.save('out.png')"
```

## Used beyond X

Despite the folder name, `avatar-dark.svg` is the **source for the Codex/ChatGPT
plugin's listing assets** — `plugin/assets/{logo.png,icon.png,icon.svg}` are the
same mark, re-rendered (not upscaled) at 1024 and 512. Change the mark here and
those need regenerating; see `plugin/README.md`.
