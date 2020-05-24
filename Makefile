
SHELL=/bin/bash

# name of the docker repository
DOCKER_REPO=motlib/dbloc

# has of the last git commit
GIT_COMMIT=$(shell git rev-parse HEAD)


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

	docker build --build-arg CN_MIRROR=${CN_MIRROR} --tag $(DOCKER_REPO):$(GIT_COMMIT) .

	git checkout dbloc_project/versioninfo.py

	echo -e "\nINFO: Created docker image $(DOCKER_REPO):$(GIT_COMMIT).\n"


# Build and run the docker image
.PHONY: docker_run
docker_run: docker
	docker run --rm --name dbloc -p 8000:80 $(DOCKER_REPO):$(GIT_COMMIT)


# publish the docker image to docker hub. This is intended to be run as a
# TravisCI job
.PHONY: docker_publish
docker_publish: docker
	if [ -z "$${TRAVIS_BUILD_NUMBER}" ]; then echo "ERROR: Please only run as TravisCI job."; exit 1; fi

	if [ -z "$${DOCKER_USER}" ]; then echo "ERROR: DOCKER_USER not set."; exit 1; fi;
	if [ -z "$${DOCKER_PASS}" ]; then echo "ERROR: DOCKER_PASS not set."; exit 1; fi;

	export TAG=`if [ "$${TRAVIS_BRANCH}" == "master" ]; then echo "latest"; else echo $${TRAVIS_BRANCH} ; fi`; \
	docker login -u $${DOCKER_USER} -p $${DOCKER_PASS}; \
	docker tag $(DOCKER_REPO):$(GIT_COMMIT) $(DOCKER_REPO):$${TAG}; \
	docker tag $(DOCKER_REPO):$(GIT_COMMIT) $(DOCKER_REPO):travis-$${TRAVIS_BUILD_NUMBER}; \
	docker push $(DOCKER_REPO);


# Run pylint to check source code
lint:
	source ./.venv/bin/activate; \
	pylint --rcfile pylintrc \
	    --output-format colorized \
	    --load-plugins pylint_django \
	    dbloc loc
