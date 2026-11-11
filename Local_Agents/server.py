"""Local runner for the Northstar Seafood tabletop agents.

Serves a small chat UI on http://127.0.0.1:8765 and forwards each chat to a
local Ollama model, with the agent's prompt from ../Agents/prompts/*.md as the
system message. Standard library only: run with `python server.py`.
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
# The prompts are shared with the Copilot Studio version in ../Agents/prompts.
PROMPTS = Path(os.environ.get("NS_PROMPTS", HERE.parent / "Agents" / "prompts")).resolve()
HOST, PORT = "127.0.0.1", int(os.environ.get("NS_PORT", "8765"))
OLLAMA = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
if not OLLAMA.startswith("http"):
    OLLAMA = "http://" + OLLAMA

# Preferred models, best first. The first one that is installed is the default.
PREFERRED = ["qwen2.5:14b", "qwen2.5:7b", "llama3.1:8b", "llama3:latest", "llama3"]

# Model settings. Low temperature keeps the facts and flag rules steadier.
OPTIONS = {"temperature": 0.4, "num_ctx": 8192}

# In-character greetings from the README (optional step 7). System agents have none.
GREETINGS = {
    "01": "Oh, hi… is this about my ticket?",
    "02": "Help desk, Tomas speaking.",
    "03": "Yes? I've got five minutes.",
    "04": "Good, you're here. Let's get started.",
}

TEXT_BLOCK = re.compile(r"^```text\s*\n(.*?)\n```", re.S | re.M)


def load_agents():
    agents = []
    for f in sorted(PROMPTS.glob("*.md")):
        raw = f.read_text(encoding="utf-8")
        m = TEXT_BLOCK.search(raw)
        if not m:
            print(f"! skipped {f.name}: no ```text block found", file=sys.stderr)
            continue
        title = raw.splitlines()[0].lstrip("# ").strip()
        num = f.name[:2]
        agents.append({
            "id": f.stem,
            "title": title,
            "kind": "system" if title.lower().startswith("system") else "persona",
            "greeting": GREETINGS.get(num, ""),
            "prompt": m.group(1).strip(),
        })
    return agents


def ollama_get(path):
    with urllib.request.urlopen(OLLAMA + path, timeout=5) as r:
        return json.loads(r.read())


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # keep the console quiet
        pass

    def send_json(self, obj, status=200):
        body = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            body = (HERE / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/api/agents":
            # Prompts stay on the server; the page only needs names and greetings.
            self.send_json([{k: a[k] for k in ("id", "title", "kind", "greeting")}
                            for a in load_agents()])
        elif self.path == "/api/models":
            try:
                names = [m["name"] for m in ollama_get("/api/tags").get("models", [])]
            except Exception as e:
                return self.send_json({"error": f"Ollama is not reachable at {OLLAMA} ({e}). "
                                                "Start the Ollama app and reload."}, 502)
            default = next((p for p in PREFERRED if p in names), names[0] if names else None)
            self.send_json({"models": names, "default": default})
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != "/api/chat":
            return self.send_error(404)
        req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
        agent = next((a for a in load_agents() if a["id"] == req.get("agent")), None)
        if not agent:
            return self.send_json({"error": "unknown agent"}, 400)
        history = [m for m in req.get("messages", [])
                   if m.get("role") in ("user", "assistant") and isinstance(m.get("content"), str)]
        payload = {
            "model": req.get("model"),
            "messages": [{"role": "system", "content": agent["prompt"]}] + history,
            "stream": True,
            "options": OPTIONS,
        }
        upstream = urllib.request.Request(OLLAMA + "/api/chat", data=json.dumps(payload).encode(),
                                          headers={"Content-Type": "application/json"})
        try:
            resp = urllib.request.urlopen(upstream, timeout=600)
        except urllib.error.HTTPError as e:
            return self.send_json({"error": f"Ollama error {e.code}: {e.read().decode(errors='replace')}"}, 502)
        except Exception as e:
            return self.send_json({"error": f"Ollama is not reachable at {OLLAMA} ({e})"}, 502)

        # Relay Ollama's NDJSON stream as plain text chunks.
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        try:
            with resp:
                for line in resp:
                    if not line.strip():
                        continue
                    chunk = json.loads(line)
                    if chunk.get("error"):
                        self.wfile.write(f"\n[Ollama error: {chunk['error']}]".encode())
                        break
                    text = chunk.get("message", {}).get("content", "")
                    if text:
                        self.wfile.write(text.encode())
                        self.wfile.flush()
                    if chunk.get("done"):
                        break
        except (BrokenPipeError, ConnectionResetError):
            pass  # the page stopped or reset the reply


def main():
    agents = load_agents()
    print(f"Loaded {len(agents)} agents from {PROMPTS}")
    if not agents:
        sys.exit("No agents found. Run this from the repo's Local_Agents folder, "
                 "or set NS_PROMPTS to the folder that holds the prompt .md files.")
    try:
        ollama_get("/api/tags")
        print(f"Ollama OK at {OLLAMA}")
    except Exception:
        print(f"! Ollama not reachable at {OLLAMA} - start the Ollama app first.")
    url = f"http://{HOST}:{PORT}"
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Open {url}   (Ctrl+C to stop)")
    if "--no-browser" not in sys.argv:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
