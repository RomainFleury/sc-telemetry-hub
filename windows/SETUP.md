# Windows setup

Scripts and flow are modeled on [libthirdspacevest-simhub](https://github.com/RomainFleury/libthirdspacevest-simhub) (`windows/check-setup.bat`, `windows/setup/*.bat`, optional `windows/.env.bat`).

## Prerequisites

- **Python 3.10+** from [python.org](https://www.python.org/downloads/) (enable **Add to PATH**), or the **py** launcher.
- **Node.js 18+** LTS from [nodejs.org](https://nodejs.org/).
- **Yarn** via **Corepack** (ships with Node 16.10+):

```bat
corepack enable
```

## First-time setup

1. Double-click **`windows\check-setup.bat`** (or run it from `cmd`).  
   It runs `setup\check-python.bat`, `check-node.bat`, `check-yarn.bat`, `check-python-packages.bat`, and `check-web-dependencies.bat`.
2. If prompted, allow it to create **`windows\.env.bat`** with `STH_PYTHON=...` so every script uses the same interpreter.
3. Or copy **`windows\.env.bat.example`** to **`windows\.env.bat`** and edit `STH_PYTHON` yourself.

`STH_PYTHON` is this project’s equivalent of the vest project’s `TSV_PYTHON`: a single command line used for `pip install -e .` and `python -m sc_telemetry.cli`.

## Install dependencies only

- **`windows\install-deps.bat`** — `pip install -e` in `daemon\`, then `yarn install` in `web\`.

## Run

- **`windows\start-daemon.bat`** — telemetry daemon (UDP 33740 in, TCP 5050 / UDP 5555 out).
- **`windows\start-ui.bat`** — Vite + Electron dev for `web\`.
- **`windows\start-all.bat`** — new `cmd` window for the daemon, then starts the UI in the current window.

## Troubleshooting

- **`python` not found** — Reinstall Python with “Add to PATH”, or set `STH_PYTHON` to the full path of `python.exe` in `windows\.env.bat`.
- **`yarn` not found** — Run `corepack enable` in a terminal, then reopen `cmd`.
- **Wrong Python version** — Set `STH_PYTHON=py -3.12` (or your installed 3.10+ tag) in `windows\.env.bat`.
