start:
	poetry run jupyter-lab

lint:
	pre-commit run --all-files
