.PHONY: install

install:
	apt update -y
	apt install python3-venv python3-tk -y
	mkdir -p .venv/
	python3 -m venv .venv/
	.venv/bin/pip install --extra-index-url https://pypi-nightly.tensorflow.org/simple --pre TTS
	.venv/bin/pip install audiosegment audio-separator onnxruntime pygame sounddevice soundfile

uninstall:
	rm -rf .venv/

uninstall-venv:
	apt remove python3-venv -y

uninstall-tk:
	apt remove python3-tk -y

uninstall-all: uninstall-venv uninstall-tk uninstall

run:
	.venv/bin/python3 app/main.py

clean:
	find .tmp/ ! -name '.gitkeep' -type f -exec rm -f {} +
	find outputs/ ! -name '.gitkeep' -type f -exec rm -f {} +
	find voice_samples/ ! -name '.gitkeep' -type f -exec rm -f {} +
	find app/ -name '__pycache__' -type d -exec rm -rf {} +