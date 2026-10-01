.PHONY: local build publication-dates test

HUGO ?= hugo

local: publication-dates
	$(HUGO) serve -D -F --config hugo.toml,.publication-dates.json

publication-dates:
	uv run scripts/publication_dates.py

build: publication-dates
	$(HUGO) --config hugo.toml,.publication-dates.json

test:
	HUGO_BIN=$(HUGO) uv run --with PyYAML==6.0.3 --python 3.12.14 python -m unittest discover -s tests
