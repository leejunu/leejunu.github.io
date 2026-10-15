#!/usr/bin/env python3
"""Small dependency-free development server with browser live reload."""

from __future__ import annotations

import argparse
import html
import json
import os
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path.cwd().resolve()
IGNORED_DIRECTORIES = {".git", "__pycache__"}
RELOAD_SCRIPT = """
<script>
(() => {
  let version = __VERSION__;

  async function checkForChanges() {
    try {
      const response = await fetch('/__live_reload_version', { cache: 'no-store' });
      const nextVersion = await response.text();
      if (nextVersion !== version) {
        window.location.reload();
        return;
      }
      version = nextVersion;
    } catch (_) {
      // The server may be restarting; the next poll will try again.
    }
  }

  window.setInterval(checkForChanges, 500);
})();
</script>
"""


def site_version() -> str:
    """Return a token that changes whenever a site file is updated."""
    latest = 0

    for directory, directory_names, file_names in os.walk(ROOT):
        directory_names[:] = [
            name for name in directory_names if name not in IGNORED_DIRECTORIES
        ]

        for file_name in file_names:
            path = Path(directory, file_name)
            try:
                latest = max(latest, path.stat().st_mtime_ns)
            except OSError:
                pass

    return str(latest)


class LiveReloadHandler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self) -> None:
        if urlparse(self.path).path == "/__live_reload_version":
            payload = site_version().encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        requested_path = Path(self.translate_path(self.path))
        if requested_path.is_dir():
            requested_path /= "index.html"

        if requested_path.is_file() and requested_path.suffix.lower() in {".html", ".htm"}:
            self._serve_html(requested_path)
            return

        super().do_GET()

    def _serve_html(self, path: Path) -> None:
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, html.escape(str(error)))
            return

        reload_script = RELOAD_SCRIPT.replace("__VERSION__", json.dumps(site_version()))
        closing_body = content.lower().rfind("</body>")
        if closing_body >= 0:
            content = content[:closing_body] + reload_script + content[closing_body:]
        else:
            content += reload_script

        payload = content.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, message_format: str, *args: object) -> None:
        if args and str(args[0]).startswith("GET /__live_reload_version"):
            return
        super().log_message(message_format, *args)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=5500)
    arguments = parser.parse_args()

    server = ThreadingHTTPServer(("127.0.0.1", arguments.port), LiveReloadHandler)
    print(f"Serving {ROOT}")
    print(f"Open http://localhost:{arguments.port}")
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
