
SHELL=/bin/bash

# Remove and create a new virtualenv with all dependencies installed.
.PHONY: setup
setup:
	rm -rf .venv; \
	python3 -m venv .venv; \
	source ./.venv/bin/activate; \
	python -m pip install -r requirements/dev.txt;


# Build the docker image
.PHONY: docker
docker:
	tools/update-version.sh

	docker build --tag dbloc .

	git checkout dbloc/versioninfo.py


# Build and run the docker image
.PHONY: docker_run
docker_run: docker
	docker run --rm --name dbloc -p 8000:80 dbloc


# Run pylint to check source code
lint:
	source ./.venv/bin/activate; \
	pylint --rcfile pylintrc \
	    --output-format colorized \
	    --load-plugins pylint_django \
	    dbloc loc
