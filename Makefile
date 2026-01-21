.PHONY: help install test lint format clean package deploy

help:
	@echo "Available commands:"
	@echo "  make install   - Install dependencies"
	@echo "  make test      - Run tests"
	@echo "  make lint      - Run linting"
	@echo "  make format    - Format code"
	@echo "  make clean     - Clean build artifacts"
	@echo "  make package   - Package lambdas for deployment"
	@echo "  make deploy    - Deploy infrastructure with Terraform"

install:
	pip install -r requirements.txt

test:
	pytest

coverage:
	pytest
	@echo "Coverage reports generated:"
	@echo "  - Terminal: Above"
	@echo "  - HTML: htmlcov/index.html"
	@echo "  - XML (for SonarQube): coverage.xml"

sonar:
	@echo "Running SonarQube analysis..."
	@which sonar-scanner > /dev/null || (echo "Error: sonar-scanner not found. Install it first." && exit 1)
	sonar-scanner

lint:
	flake8 src tests
	pylint src

format:
	black src tests

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov
	rm -rf lambda-packages/*.zip

package:
	@echo "Packaging Auth Lambda..."
	@mkdir -p lambda-packages
	@cd src && zip -r ../lambda-packages/auth_lambda.zip auth_lambda/
	@cd lambda-packages && pip install -r ../requirements.txt -t . && zip -ur auth_lambda.zip . -x "*.pyc" "__pycache__/*"
	
	@echo "Packaging Alert Lambda..."
	@cd src && zip -r ../lambda-packages/alert_lambda.zip alert_lambda/
	@cd lambda-packages && zip -ur alert_lambda.zip . -x "*.pyc" "__pycache__/*"
	
	@echo "Lambda packages created successfully!"

deploy:
	@echo "Deploying infrastructure with Terraform..."
	@cd deploy/terraform && terraform init
	@cd deploy/terraform && terraform plan
	@cd deploy/terraform && terraform apply
