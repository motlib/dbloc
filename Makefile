
# Build the docker image
.PHONY: docker
docker:
	docker build --tag dbloc .


# Build and run the docker image
docker_run: docker
	docker run --rm --name dbloc -p 8000:80 dbloc
