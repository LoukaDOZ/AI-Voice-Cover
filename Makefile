.PHONY: install

install:
	apt install python3-tk
	python3 -m pip install -r requirement.txt
	# python3 -m pip install --extra-index-url https://pypi-nightly.tensorflow.org/simple --pre TTS
	# python3 -m pip install audiosegment audio-separator onnxruntime pygame

uninstall:
	apt remove python3-tk
	python3 -m pip uninstall -r requirement.txt
	# python3 -m pip uninstall --extra-index-url https://pypi-nightly.tensorflow.org/simple --pre TTS
	# python3 -m pip uninstall audiosegment audio-separator onnxruntime pygame

run:
	python app/main.py

clean:
	find .tmp/ ! -name '.gitkeep' -type f -exec rm -f {} +
	find outputs/ ! -name '.gitkeep' -type f -exec rm -f {} +
	find app/ -name '__pycache__' -type d -exec rm -rf {} +