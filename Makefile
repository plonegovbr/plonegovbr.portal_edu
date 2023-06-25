### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

# Set distributions still in development
DISTRIBUTIONS="portal_edu"

# Docker Image name
IMAGE_NAME=ghcr.io/plonegovbr/portal_edu
IMAGE_TAG=latest

PLONE6=6.0-latest

# Python checks
PYTHON?=python3

# installed?
ifeq (, $(shell which $(PYTHON) ))
  $(error "PYTHON=$(PYTHON) not found in $(PATH)")
endif

# version ok?
PYTHON_VERSION_MIN=3.8
PYTHON_VERSION_OK=$(shell $(PYTHON) -c "import sys; print((int(sys.version_info[0]), int(sys.version_info[1])) >= tuple(map(int, '$(PYTHON_VERSION_MIN)'.split('.'))))")
ifeq ($(PYTHON_VERSION_OK),0)
  $(error "Need python $(PYTHON_VERSION) >= $(PYTHON_VERSION_MIN)")
endif

BACKEND_FOLDER=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

GIT_FOLDER=$(BACKEND_FOLDER)/.git


all: build

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

bin/pip bin/tox bin/mxdev:
	@echo "$(GREEN)==> Setup Virtual Env$(RESET)"
	$(PYTHON) -m venv .
	bin/pip install -U "pip" "wheel" "cookiecutter" "mxdev" "tox" "pre-commit"
	if [ -d $(GIT_FOLDER) ]; then bin/pre-commit install; else echo "$(RED) Not installing pre-commit$(RESET)";fi

constraints-mxdev.txt:  bin/tox
	bin/tox -e init

.PHONY: config
config: bin/pip  ## Create instance configuration
	@echo "$(GREEN)==> Create instance configuration$(RESET)"
	bin/cookiecutter -f --no-input --config-file instance.yaml gh:plone/cookiecutter-zope-instance

.PHONY: build-dev
build-dev: config constraints-mxdev.txt ## pip install Plone packages
	@echo "$(GREEN)==> Setup Build$(RESET)"
	bin/pip install -r requirements-mxdev.txt

.PHONY: install
install: build-dev ## Install Plone 6.0

.PHONY: build
build: build-dev ## Install Plone 6.0

.PHONY: clean
clean: ## Remove old virtualenv and creates a new one
	@echo "$(RED)==> Cleaning environment and build$(RESET)"
	rm -rf bin lib lib64 include share etc var inituser pyvenv.cfg .installed.cfg instance .tox .pytest_cache requirements-mxdev.txt constraints-mxdev.txt

.PHONY: start
start: ## Start a Plone instance on localhost:8080
	DEVELOP_DISTRIBUTIONS=$(DISTRIBUTIONS) PYTHONWARNINGS=ignore ./bin/runwsgi instance/etc/zope.ini

.PHONY: console
console: ## Start a zope console
	DEVELOP_DISTRIBUTIONS=$(DISTRIBUTIONS) PYTHONWARNINGS=ignore ./bin/zconsole debug instance/etc/zope.conf

.PHONY: format
format: bin/tox ## Format the codebase according to our standards
	@echo "$(GREEN)==> Format codebase$(RESET)"
	bin/tox -e format

.PHONY: lint
lint: ## check code style
	bin/tox -e lint

# i18n
bin/i18ndude: bin/pip
	@echo "$(GREEN)==> Install translation tools$(RESET)"
	bin/pip install i18ndude

.PHONY: i18n
i18n: bin/i18ndude ## Update locales
	@echo "$(GREEN)==> Updating locales$(RESET)"
	bin/update_dist_locale

# Tests
.PHONY: test
test: bin/tox constraints-mxdev.txt ## run tests
	DEVELOP_DISTRIBUTIONS=$(DISTRIBUTIONS) bin/tox -e test

.PHONY: test-coverage
test-coverage: bin/tox constraints-mxdev.txt ## run tests with coverage
	DEVELOP_DISTRIBUTIONS=$(DISTRIBUTIONS) bin/tox -e coverage

# Docker image
.PHONY: build-image
build-image:  ## Build Docker Image
	@DOCKER_BUILDKIT=1 docker build . -t $(IMAGE_NAME):$(IMAGE_TAG) -f Dockerfile --build-arg PLONE_VERSION=$(PLONE_VERSION)

.PHONY: run-image
run-image:  build-image  ## Build Docker Image
	docker run --rm -it -p 8080:8080 $(IMAGE_NAME):$(IMAGE_TAG)
