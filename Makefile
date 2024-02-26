SHELL := /bin/bash

init:
	python3 -m venv hackaton_3_venv; \
	source hackaton_3_venv/bin/activate; \
	pip install --upgrade pip; \
	pip install -r requirements.txt

