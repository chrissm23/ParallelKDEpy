import os
from pathlib import Path
import runpy
from sphinx.util import logging

logger = logging.getLogger(__name__)


def _run_example(app, config):
    if os.getenv("CI"):  # GitHub Actions sets this
        return

    srcdir = Path(app.srcdir)
    script = srcdir / "scripts" / "plot_kde.py"
    if not script.exists():
        logger.warning("[auto_examples] Script not found: %s", script)
        return

    logger.info("[auto_examples] Running example script: %s", script)
    try:
        runpy.run_path(str(script), run_name="__main__")
    except Exception as e:
        logger.error("[auto_examples] Script failed: %s", e)
        raise

    out = srcdir / "_static" / "figures" / "getting-started.png"
    logger.info("[auto_examples] Expected outut: %s (exists=%s)", out, out.exists())


def setup(app):
    app.connect("config-inited", _run_example)
    return {"version": "0.1", "parallel_read_safe": True}
