# Makefile

.PHONY: test build installer

# Run unit tests with Pytest
test:
	poetry run pytest --junitxml=testLog.xml --cov=coverage_ai --cov-report=xml:cobertura.xml --cov-report=term --cov-fail-under=70 --log-cli-level=INFO

# Use Python Black to format python files
format:
	black .

# Generate wheel file using poetry build command
build:
	poetry build

# Build an executable using Pyinstaller
installer:
	poetry run pyinstaller \
		--add-data "coverage_ai/version.txt:." \
		--add-data "coverage_ai/settings/language_extensions.toml:." \
		--add-data "coverage_ai/settings/test_generation_prompt.toml:." \
		--add-data "coverage_ai/settings/analyze_suite_test_headers_indentation.toml:." \
		--add-data "coverage_ai/settings/analyze_suite_test_insert_line.toml:." \
		--hidden-import=tiktoken_ext.openai_public \
		--hidden-import=tiktoken_ext \
		--hidden-import=wandb \
		--hidden-import=wandb_gql \
		--onefile \
		--name coverage-ai \
		coverage_ai/main.py
