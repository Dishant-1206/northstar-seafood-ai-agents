#!/bin/sh
# Start the Northstar tabletop agents on macOS or Linux (needs Python 3 and Ollama running).
cd "$(dirname "$0")" || exit 1
exec python3 server.py "$@"
