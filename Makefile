
SHELL=/bin/bash

# Remove and create a new virtualenv with all dependencies installed.
.PHONY: setup
setup:
	rm -rf .venv; \
	python3 -m venv .venv; \
	source ./.venv/bin/activate; \
	python -m pip install -r requirements/dev.txt;


# set to
ifeq (${TRAVIS},true)
  CN_MIRROR=0
else
  CN_MIRROR=1
endif

# Build the docker image
.PHONY: docker
docker:
	tools/update-version.sh

	docker build --build-arg CN_MIRROR=${CN_MIRROR} --tag dbloc .

	git checkout dbloc_project/versioninfo.py


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
