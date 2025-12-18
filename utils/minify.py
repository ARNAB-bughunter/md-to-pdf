from csscompressor import compress
from jsmin import jsmin
import htmlmin
from pathlib import Path
import shutil


SRC_DIR = Path("static")
DST_DIR = Path("static_min")


def minify_static_files():
    if DST_DIR.exists():
        shutil.rmtree(DST_DIR)
    
    DST_DIR.mkdir(exist_ok=True)

    for path in SRC_DIR.rglob("*"):
        if path.is_dir():
            continue

        target = DST_DIR / path.relative_to(SRC_DIR)
        target.parent.mkdir(parents=True, exist_ok=True)

        content = path.read_text(encoding="utf-8")

        if path.suffix == ".css":
            content = compress(content)

        elif path.suffix == ".js":
            content = jsmin(content)

        elif path.suffix == ".html":
            content = htmlmin.minify(
                content,
                remove_comments=True,
                remove_empty_space=True,
            )

        target.write_text(content, encoding="utf-8")