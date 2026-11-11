PY ?= python3

.PHONY: help install capture cards judge aggregate report slide all clean test
help:
	@echo "make install    install Python deps"
	@echo "make capture    fetch paired search results (needs .env)"
	@echo "make cards      build blind evidence cards"
	@echo "make judge      score with your judge model, both orders"
	@echo "make aggregate  summary table + JSON"
	@echo "make report     HTML + PDF from out/REPORT.md"
	@echo "make slide      re-render assets/slide.png from assets/slide.html"
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

# Re-render the one-slide summary. Pure Chrome headless, no Python deps.
# Set BROWSER_BIN if Chrome is not in the default macOS location.
BROWSER_BIN ?= $(shell \
	for p in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
	         "/Applications/Chromium.app/Contents/MacOS/Chromium" \
	         "$$(command -v google-chrome)" "$$(command -v chromium)" \
	         "$$(command -v chromium-browser)"; do \
	  [ -x "$$p" ] && echo "$$p" && break; done)
slide:
	@[ -n "$(BROWSER_BIN)" ] || { echo "No Chrome/Chromium found; set BROWSER_BIN=..."; exit 1; }
	"$(BROWSER_BIN)" --headless --disable-gpu --hide-scrollbars \
	  --force-device-scale-factor=2 --window-size=1600,900 \
	  --screenshot=assets/slide.png "file://$(CURDIR)/assets/slide.html"
	@echo "assets/slide.png  (3200x1800)"

test:
	$(PY) -m pytest -q tests || $(PY) -m unittest discover -s tests -v

clean:
	rm -rf data/raw data/cards data/judged out dist __pycache__ src/bench/__pycache__
