# Makefile

# General settings
IMAGE_NAME=lehrstuhlkesdogan/praktomat
PRAKTOMAT_REPO=https://github.com/ITSec-UR/praktomat

# Building settings
UBUNTU_VERSION=noble
JAVA_VERSION=21

PRAKTOMAT_DIR := $(notdir $(PRAKTOMAT_REPO))
PRAKTOMAT_COMMIT := $(shell git ls-remote $(PRAKTOMAT_REPO) HEAD | awk '{ print substr($$1,1,7) }')
TAG := $(UBUNTU_VERSION)-jdk$(JAVA_VERSION)-git$(PRAKTOMAT_COMMIT)

NO_CACHE ?=
DOCKER_NO_CACHE := $(if $(NO_CACHE),--no-cache,)

.PHONY: all clone build push clean

all: build

clone:
	@if [ ! -d "$(PRAKTOMAT_DIR)" ]; then \
		git clone --recursive $(PRAKTOMAT_REPO) $(PRAKTOMAT_DIR); \
	else \
		echo "$(PRAKTOMAT_DIR) already cloned."; \
	fi

build-unchecked: clone
	docker build $(DOCKER_NO_CACHE) \
		--build-arg UBUNTU_VERSION=$(UBUNTU_VERSION) \
		--build-arg JAVA_VERSION=$(JAVA_VERSION) \
		--build-arg PRAKTOMAT_DIR=$(PRAKTOMAT_DIR) \
		-t $(IMAGE_NAME):$(TAG) .
	docker tag $(IMAGE_NAME):$(TAG) $(IMAGE_NAME):latest

# Build image only if it doesn't exist
build:
	@echo "Building $(IMAGE_NAME):$(TAG) ..."
	@if docker images $(IMAGE_NAME):$(TAG) | grep -q $(TAG); then \
		echo "Image $(IMAGE_NAME):$(TAG) already exists. Skipping build."; \
	else \
		$(MAKE) build-unchecked; \
	fi

# Rebuild the image (force clean rebuild)
rebuild: clean
	@echo "Rebuilding $(IMAGE_NAME):$(TAG) ..."
	$(MAKE) build-unchecked

push: build
	docker push $(IMAGE_NAME):$(TAG)
	docker push $(IMAGE_NAME):latest
	echo "Successfully pushed $(IMAGE_NAME):$(TAG)"

clean:
	@echo "Cleaning up Docker images ($(IMAGE_NAME):$(TAG)) ..."
	rm -rf $(PRAKTOMAT_DIR)
	-docker rmi $(IMAGE_NAME):latest
	-docker rmi $(IMAGE_NAME):$(TAG)
