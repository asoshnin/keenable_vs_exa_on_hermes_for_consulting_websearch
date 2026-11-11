PY ?= python3

.PHONY: help install capture cards judge aggregate report all clean test
help:
	@echo "make install    install Python deps"
	@echo "make capture    fetch paired search results (needs .env)"
	@echo "make cards      build blind evidence cards"
	@echo "make judge      score with your judge model, both orders"
	@echo "make aggregate  summary table + JSON"
	@echo "make report     HTML + PDF from out/REPORT.md"
	@echo "make all        capture -> cards -> judge -> aggregate"
	@echo "make test       offline unit tests (no network)"

install:
	$(PY) -m pip install -r requirements.txt

capture:   ; $(PY) run.py capture
cards:     ; $(PY) run.py cards
judge:     ; $(PY) run.py judge
aggregate: ; $(PY) run.py aggregate
report:    ; $(PY) run.py render
all:       ; $(PY) run.py all

test:
	$(PY) -m pytest -q tests || $(PY) -m unittest discover -s tests -v

clean:
	rm -rf data/raw data/cards data/judged out dist __pycache__ src/bench/__pycache__
