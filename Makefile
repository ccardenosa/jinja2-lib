# Makefile

all: install test

install-git-prehooks:
	 test -f .pre-commit-config.yaml && pre-commit install

clean-git-prehooks:
	pre-commit clean
	rm -f .git/hooks/pre-commit

install: venv
	: # Activate venv and install somthing inside
	source .venv/bin/activate && python3 -m pip install --upgrade pip && pip install -r requirements.txt

venv:
	: # Create .venv if it doesn't exist
	: # test -d .venv || virtualenv -p python3 --no-site-packages .venv
	test -d .venv || python3 -m venv .venv

version:
	: # Run your app here, e.g
	source .venv/bin/activate && pip -V

	: # Exec multiple commands
	source .venv/bin/activate && (\
		python3 -c 'import sys; print(sys.prefix)'; \
		echo ; \
		pip3 -V ;\
	)

test:
	: # Running Testing...
	source .venv/bin/activate && (\
		export PYTHONPATH=${PWD}:${PATH}; \
		pytest tests/ \
	)

clean:
	find . -type f -iname '*.pyc' -delete
