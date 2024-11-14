# AI Voice Cover

Python app to replace an audio voice with another one using AI.
![App screenshot](.assets/app.png)

AI models:
- [Audio Separator](https://github.com/nomadkaraoke/python-audio-separator) (default model)
- [Coqui.ai TTS](https://github.com/coqui-ai/TTS) (freevc24)

## Usage
### Requirements

- Python >= 3.11
- Make

### Installed packages

- TTS
- Audio Separator
- AudioSegment
- Tkinter
- Venv

### Makefile

| Command               | Description                                |
|-----------------------|--------------------------------------------|
| `make install`        | Install Venv, Tkinter and Python libraries |
| `make uninstall`      | Uninstall libraries                        |
| `make uninstall-venv` | Uninstall Venv                             |
| `make uninstall-tk`   | Uninstall Tkinter                          |
| `make uninstall-all`  | Uninstall Venv, Tkinter and libraries      |
| `make run`            | Start project                              |
| `make clean`          | Clean project                              |

### Install

If needed, install requirements using:
```bash
apt update -y
apt install build-essential libssl-dev libffi-dev libglib2.0-0 python3.11 python-dev-is-python3 make -y
```

To install project libraries, use:
```bash
make install
```

### Run

To run the project, use:
```bash
make run
```

### Uninstall

To unistall the project libraries, use:
```bash
make uninstall
```

To unistall the project libraries and Venv, use:
```bash
make uninstall
make uninstall-venv
```

To unistall the project libraries and Tkinter, use:
```bash
make uninstall
make uninstall-tk
```

To unistall everything, use:
```bash
make uninstall-all
```