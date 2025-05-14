# Makefile

IMAGE_NAME=lehrstuhlkesdogan/praktomat
PRAKTOMAT_REPO=https://github.com/ITSec-UR/praktomat
PRAKTOMAT_DIR=praktomat

APP_VERSION_FILE=src/settings/version.py
RAW_APP_VERSION_FILE := $(PRAKTOMAT_REPO)/raw/master/$(APP_VERSION_FILE)

BASE_TAG := $(shell git describe --tags $(shell git rev-list --tags --max-count=1) || echo "dev")
APP_VERSION := $(shell wget -q -O - $(RAW_APP_VERSION_FILE) | grep '__version__' | cut -d '"' -f2)
TAG := $(if $(APP_VERSION),$(APP_VERSION)-$(BASE_TAG),$(BASE_TAG))

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

build: clone
	@if docker images $(IMAGE_NAME):$(TAG) | grep -q $(TAG); then \
		echo "Image $(IMAGE_NAME):$(TAG) already exists. Skipping build."; \
	else \
		echo "Building $(IMAGE_NAME):$(TAG)..."; \
		docker build $(DOCKER_NO_CACHE) -t $(IMAGE_NAME):$(TAG) .; \
		docker tag $(IMAGE_NAME):$(TAG) $(IMAGE_NAME):latest; \
	fi

# Rebuild the image (force clean rebuild)
rebuild: clone
	@echo "Rebuilding $(IMAGE_NAME):$(TAG)..."
	docker build $(DOCKER_NO_CACHE) -t $(IMAGE_NAME):$(TAG) .
	docker tag $(IMAGE_NAME):$(TAG) $(IMAGE_NAME):latest

push: build
	docker push $(IMAGE_NAME):$(TAG)
	docker push $(IMAGE_NAME):latest
	echo "Successfully pushed $(IMAGE_NAME):$(TAG)"

clean:
	@echo "Cleaning up Docker images ($(IMAGE_NAME):$(TAG))..."
	rm -rf $(PRAKTOMAT_DIR)
	docker rmi $(IMAGE_NAME):latest 2>/dev/null || true
	docker rmi $(IMAGE_NAME):$(TAG) 2>/dev/null || true
