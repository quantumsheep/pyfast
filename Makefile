.PHONY: generate
generate:
	@echo "Generating visitor..."
	@java -jar ./bin/antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor -no-listener src/parser/grammar/*.g4

	@echo "Adding # type: ignore to the generated files..."
	@sed -i '' '1s/^/# type: ignore\n/' src/parser/grammar/*.py

.PHONY: test
test:
	@poetry run pytest --no-header -v --tb=line
