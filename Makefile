SHELL := /bin/bash

init:
	python3 -m venv hackaton_venv; \
	source hackaton_venv/bin/activate; \
	pip install --upgrade pip; \
	pip install -r requirements/requirements.txt

