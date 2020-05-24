
SHELL=/bin/bash

# name of the docker repository
DOCKER_REPO=motlib/dbloc

# current branch and hash of the last git commit
GIT_COMMIT=$(shell git rev-parse HEAD)
GIT_BRANCH=$(shell git branch --show-current)

# if we build the master branch, it's a release. Otherwise it's a test
ifeq ($(GIT_BRANCH),master)
  DOCKER_TAG=latest
else
  DOCKER_TAG=testing
endif

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

	docker build --build-arg CN_MIRROR=${CN_MIRROR} --tag $(DOCKER_REPO):$(DOCKER_TAG) .

	git checkout dbloc_project/versioninfo.py

	echo -e "\nINFO: Created docker image '$(DOCKER_REPO):$(DOCKER_TAG)'.\n"


# Build and run the docker image
.PHONY: docker_run
docker_run: docker
	docker run --rm --name dbloc -p 8000:80 $(DOCKER_REPO):$(DOCKER_TAG)


# publish the docker image to docker hub. This is intended to be run as a
# TravisCI job
.PHONY: docker_publish
docker_publish: docker
	[ -n "$${TRAVIS_BUILD_NUMBER}" ] \
	  || ( echo "ERROR: Please only run as TravisCI job."; exit 1; )

	[ -n "$${DOCKER_USER}" ] \
	  || ( echo "ERROR: DOCKER_USER not set."; exit 1; )
	[ -n "$${DOCKER_PASS}" ] \
	  || ( echo "ERROR: DOCKER_PASS not set."; exit 1; )

	echo $${DOCKER_PASS} | docker login --username $${DOCKER_USER} --password-stdin; \
	docker push $(DOCKER_REPO); \
	docker logout

	echo -e "\nINFO: Pushed docker image '$(DOCKER_REPO):$(DOCKER_TAG)'.\n"


# Run pylint to check source code
lint:
	source ./.venv/bin/activate; \
	pylint --rcfile pylintrc \
	    --output-format colorized \
	    --load-plugins pylint_django \
	    dbloc loc
