# Windows helper scripts

Conventions follow **[libthirdspacevest-simhub](https://github.com/RomainFleury/libthirdspacevest-simhub)** (`windows/check-setup.bat`, `windows/setup/`, optional `.env.bat` for Python).

| Script | Purpose |
|--------|---------|
| `check-setup.bat` | Verify Python, Node, Yarn, editable `daemon` install, and `web` dependencies |
| `install-deps.bat` | `pip install -e ./daemon` + `yarn install` in `./web` |
| `start-daemon.bat` | Run `python -m sc_telemetry.cli daemon start` from `daemon/` |
| `start-ui.bat` | Run `yarn dev` in `web/` |
| `start-all.bat` | Daemon in a new console + UI in this window |
| `.env.bat.example` | Copy to `.env.bat` and set `STH_PYTHON` (this repo’s name for the shared interpreter) |

See **`SETUP.md`** for a short walkthrough.
