"""Render README locally with a GitHub-like Markdown layout."""
from pathlib import Path
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'install/readme-preview-deps'))
import markdown


def slugify(value, separator):
    value = ''.join(c for c in value.lower() if (unicodedata.category(c)[0] in 'LNM' or c in ' -_') and c != '\ufe0f')
    return re.sub(r'\s', '-', value)


source = (ROOT / 'README.md').read_text(encoding='utf-8')
source = source.replace('<div align="center">', '<div align="center" markdown="1">')
body = markdown.markdown(source, extensions=['tables', 'fenced_code', 'md_in_html', 'toc'],
                         extension_configs={'toc': {'slugify': slugify}})
body = body.replace('href="#', 'href="/install/readme-preview/index.html#')
page = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<base href="/"><title>Maa海螺肉 · README 预览</title><style>
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#fff;color:#1f2328;font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI","Microsoft YaHei",sans-serif}
.top{background:#f6f8fa;border-bottom:1px solid #d1d9e0;padding:17px max(24px,calc((100vw - 1080px)/2));font-size:14px;color:#59636e}.top strong{color:#1f2328}.shell{max-width:1080px;margin:32px auto 64px;border:1px solid #d1d9e0;border-radius:6px;overflow:hidden}.file{padding:13px 24px;background:#f6f8fa;border-bottom:1px solid #d1d9e0;font-size:14px;font-weight:600}article{padding:32px 48px 48px;overflow-wrap:break-word}
h1,h2,h3{line-height:1.3;font-weight:600;margin-top:24px;margin-bottom:16px}h1{font-size:32px;padding-bottom:.3em;border-bottom:1px solid #d1d9e0}h2{font-size:24px;padding-bottom:.3em;border-bottom:1px solid #d1d9e0;margin-top:32px}h3{font-size:20px}p,ul,ol,table,blockquote,pre{margin:0 0 16px}li+li{margin-top:5px}a{color:#0969da;text-decoration:none}a:hover{text-decoration:underline}img{max-width:100%;vertical-align:middle}hr{height:4px;border:0;background:#d1d9e0;margin:24px 0}blockquote{padding:0 16px;border-left:4px solid #d1d9e0;color:#59636e}blockquote p:last-child{margin:0}table{border-collapse:collapse;display:block;overflow:auto;width:max-content;max-width:100%}th,td{padding:7px 13px;border:1px solid #d1d9e0}th{font-weight:600}tr:nth-child(even){background:#f6f8fa}code{padding:.2em .4em;border-radius:6px;background:#eff1f3;font:85% ui-monospace,Consolas,monospace}pre{padding:16px;background:#f6f8fa;border-radius:6px;overflow:auto}pre code{padding:0;background:transparent;line-height:1.5}div[align=center] h1{border:0;margin:12px 0}div[align=center]{margin-bottom:28px}div[align=center] img{margin:4px 0 8px}
@media(max-width:700px){.shell{border:0;margin:0}.file{padding:12px 20px}article{padding:24px 20px}.top{padding:12px 20px}}
</style></head><body><header class="top"><strong>MaaHLR</strong> / README.md <span style="float:right">本地预览 · 未上传 GitHub</span></header><main class="shell"><div class="file">📖 README.md</div><article>''' + body + '</article></main></body></html>'
destination = ROOT / 'install/readme-preview/index.html'
destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_text(page, encoding='utf-8')
print(destination)
