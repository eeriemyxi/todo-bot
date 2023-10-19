WORKDIR=.

lint:
	@black $(WORKDIR)
	@ruff check $(WORKDIR) --fix
	@pre-commit run --all-files
