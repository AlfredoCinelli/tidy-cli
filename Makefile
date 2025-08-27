# Run tests
pytest:
	@sh scripts/pytest.sh $(path)

# Run linters
linters:
	@sh scripts/linters.sh $(path)

# Build package
build:
	@sh scripts/build.sh

# Development setup
publish:
	@sh scripts/publish.sh