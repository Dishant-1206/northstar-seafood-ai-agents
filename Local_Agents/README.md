# Northstar Seafood agents – run locally with Ollama

This folder runs the eight Northstar Seafood tabletop agents on your own computer, with no
Microsoft Copilot Studio account and no cloud service. A small Python server shows a chat page in
your browser and sends each conversation to a free local AI model through
[Ollama](https://ollama.com). Nothing you type leaves your machine.

The agents are the same ones as in [`../Agents`](../Agents): the server reads their instructions
straight from `Agents/prompts/*.md`, so both versions always stay in sync.

> **Facilitators:** the prompt files contain the flag codes, and `Agents/docs/walkthrough.md`
> holds the full solution. Don't give participants access to this repository during a run.

## What you need

| | Minimum | Better |
|---|---|---|
| OS | Windows 10/11, macOS 12+, or Linux | |
| RAM | 8 GB | 16 GB |
| GPU | None (runs on the CPU, but slowly) | NVIDIA with 6 GB+ VRAM, or Apple Silicon |
| Disk | About 6 GB free for one model | |
| Software | Python 3.8+, Ollama, Git (or download the ZIP) | |

You don't need to `pip install` anything. The server uses only Python's standard library.

## Setup (one time)

### 1. Install Python
- **Windows:** install from [python.org](https://www.python.org/downloads/) and tick **Add python.exe to PATH** in the installer.
- **macOS:** `brew install python`, or use the python.org installer.
- **Linux:** Python 3 is usually already installed (`python3 --version`).

### 2. Install Ollama and download a model
Install Ollama from [ollama.com/download](https://ollama.com/download) and start it. On Windows
and macOS it runs as a tray/menu-bar app. On Linux, run `ollama serve` if it isn't running as a
service.

Then download a model (about 5 GB, one time):

```bash
ollama pull qwen2.5:7b
```

### 3. Get this repository

```bash
git clone https://github.com/Dishant-1206/northstar-seafood-ai-agents.git
```

Or on GitHub choose **Code → Download ZIP** and unzip it. Keep the folder layout as it is: the
server needs the `Agents` folder next to `Local_Agents`.

## Run it

Make sure Ollama is running, then:

- **Windows:** double-click `Local_Agents\start.bat`
- **macOS / Linux:**

  ```bash
  sh Local_Agents/start.sh
  ```

- **Any OS:** in the `Local_Agents` folder, run `python server.py` (or `python3 server.py`).

The chat page opens in your browser at <http://127.0.0.1:8765>. To stop the server, press
**Ctrl+C** in its terminal window or close the window.

The first reply can take up to a minute while the model loads into memory. After that, replies
take a few seconds on a good GPU and 10–30 seconds on a laptop CPU.

## Using it

- **Personas** (Elena, Tomas, Priya, Daniel) are interviewed in plain language and open with an
  in-character greeting.
- **Systems** (FIN-WS-014, identity service, proxy/firewall, FS-01) act as simulated terminals.
  Start with `help` to see the supported commands.
- Every agent keeps its own conversation, and chats survive a page reload.
- When an agent reveals a flag (`NS{...}`), it is highlighted and added to **Flags found** with
  the time it appeared. Use this with `Agents/docs/flag_sheet.md`.
- **Reset this agent** clears one conversation and its flags.
- **New run (reset all)** clears everything before the next group.
- **Model** switches between the models you have installed.

The exercise itself (briefing, order of play, debrief) works the same as described in
[`Agents/README.md`](../Agents/README.md#running-an-exercise).

## Choosing a model

Smaller models are faster but drift out of character and miss flag rules more often than
Copilot Studio's model. Test the model you plan to use with the checklists in
`Agents/docs/test_log.md` before a real session.

| Model | Download | Notes |
|---|---|---|
| `qwen2.5:7b` | ~4.7 GB | Recommended starting point; follows instructions well |
| `llama3.1:8b` | ~4.9 GB | Good alternative |
| `qwen2.5:14b` | ~9 GB | More reliable; needs a stronger GPU or patience |

The server picks the best installed model from this list by default, and you can change it in the
page at any time.

## Settings

| Variable | Default | Meaning |
|---|---|---|
| `NS_PORT` | `8765` | Port for the chat page |
| `OLLAMA_HOST` | `http://127.0.0.1:11434` | Where Ollama is running |
| `NS_PROMPTS` | `../Agents/prompts` | Folder with the agent prompt files |

Temperature and context length are in `OPTIONS` at the top of `server.py`. Start the server with
`--no-browser` if you don't want it to open a browser tab.

## Editing agents

Edit the text block (the part between `` ```text `` and `` ``` ``) in the matching file in
`Agents/prompts/`. The server re-reads the prompts on every message, so you don't need to
restart it: reset that agent's chat and try again. If you change a fact, update every prompt that
uses it, as noted in the main README.

## Troubleshooting

| Problem | Fix |
|---|---|
| "Ollama is not reachable" | Start the Ollama app (or run `ollama serve`), then reload the page. |
| "No Ollama models installed" | Run `ollama pull qwen2.5:7b`. |
| `python` is not recognised | Reinstall Python with **Add to PATH** ticked, or try `py server.py` on Windows. |
| "No agents found" | Keep `Local_Agents` and `Agents` side by side, or set `NS_PROMPTS`. |
| Port 8765 already in use | Another copy is running, so close it, or set `NS_PORT=8766`. |
| Replies are very slow | Use a smaller model, close other heavy apps, or run on a machine with a GPU. |

## Files

```
Local_Agents/
├── server.py    Local web server; forwards chats to Ollama
├── index.html   Chat page (agent list, flags, reset buttons)
├── start.bat    Windows launcher
├── start.sh     macOS/Linux launcher
└── README.md    This file
```
