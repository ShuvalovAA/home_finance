SOURCES=./hfin
TESTS=./tests

PYPI_USER = ${pypi_user}
PYPI_PASS = ${pypi_pass}

DOCKER_IMAGE_TAG = $(or ${VERSION}, $(shell poetry version -s))
DOCKER_IMAGE = cr.yandex/crp0civq107m91j8p8a2/services/changeset:$(DOCKER_IMAGE_TAG)
DOCKER_BUILD_ARGS = --build-arg pypi_pass='$(PYPI_PASS)' --build-arg pypi_user='$(PYPI_USER)'


lint:
	flake8 --count --show-source --statistics --config=.flake8rc $(SOURCES)

lint-imports:
	PYTHONPATH=$(SOURCES) lint-imports --config=.importlinterrc

security-lint:
	bandit --ini .bandit --recursive --format=txt $(SOURCES)

imports-lint:
	isort --settings=.isort.cfg --check $(SOURCES)

sort-imports:
	isort --settings=.isort.cfg $(SOURCES)

check-lint: lint sort-imports lint-imports security-lint imports-lint

test:
	PYTHONPATH=$(SOURCES):$(PYTHONPATH) python -m pytest --cov=$(SOURCES) --cov-report=term --cov-report html --cov-config=.coveragerc $(TESTS)

build: clean
	poetry build

clean-package:
	rm -rf build/
	rm -rf dist/
	find . -type d -name '*.egg-info' | xargs rm -rf

clean: clean-package
	rm -rf tests/.pytest_cache/
	rm -f .coverage
	rm -rf htmlcov/
	find . -type d -name '__pycache__' | xargs rm -rf

docker-build:
ifneq ($(PYPI_PASS),)
ifneq ($(PYPI_USER),)
	poetry lock --no-update \
	&& docker build  --tag $(DOCKER_IMAGE) $(DOCKER_BUILD_ARGS) .
else
	@echo 'pypi_user is not set. Use: "make docker-build pypi_user=some.user pypi_pass=***"'
endif
else
	@echo 'pypi_pass is not set. Use: "make docker-build pypi_user=some.user pypi_pass=***"'
endif

docker-push:
	docker push $(DOCKER_IMAGE)

minikube-list-pods:
	@minikube kubectl -- get pods -n changeset

minikube-run-local:
	@helm install --create-namespace -n changeset changeset ./helm -f ./helm/values.local.yaml

minikube-stop-local:
	@helm uninstall changeset -n changeset


