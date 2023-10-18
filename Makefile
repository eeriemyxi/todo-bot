lint:
	ruff check . --fix
	pre-commit run --all-files
