.PHONY: install

install:
	apt install python3-tk
	python -m pip install -r requirement.txt

uninstall:
	apt remove python3-tk
	python -m pip uninstall -r requirement.txt
	# python -m pip install --extra-index-url https://pypi-nightly.tensorflow.org/simple --pre TTS
	# python -m pip install audiosegment audio-separator onnxruntime

clean:
	find .tmp/ ! -name '.gitkeep' -type f -exec rm -f {} +
	find app/ -name '__pycache__' -type d -exec rm -rf {} +