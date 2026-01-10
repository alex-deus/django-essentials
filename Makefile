.PHONY: lint install clean build upload

lint:  ## Run pre-commit on all files
	@pre-commit run --all-files

update-isort:
	@seed-isort-config

install:  ## Install package and pre-commit hooks
	@pip install poetry
	@poetry install
	@pre-commit install

clean:  ## Clean build artifacts
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@rm -rf .coverage
	@rm -rf htmlcov/
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete

bump:  ## Update version at setup.py
	@VERSION=$(v); \
	if [ -z "$$VERSION" ]; then \
		@echo "To use: make bump v=1.2.3"; \
		exit 1; \
	fi;
	@sed -i.bak -E "s/^(__version__ *= *[\"']).*([\"'])/\1$$VERSION\2/" setup.py && rm -f setup.py.bak
	@sed -i.bak -E "s/^(version *= *[\"]).*([\"])/\1$$VERSION\2/" pyproject.toml && rm -f pyproject.toml.bak

build:  ## Build package
	@python -m build

upload:  ## Upload the build to PyPI
	@twine upload --verbose dist/*
