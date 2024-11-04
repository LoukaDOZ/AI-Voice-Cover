.PHONY: install

install:
	apt install python3-tk
	python -m pip install -r requirement.txt

uninstall:
	apt remove python3-tk
	python -m pip uninstall -r requirement.txt

clean:
	@echo "TODO"